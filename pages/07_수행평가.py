# pages/region_license_dashboard.py
# Streamlit app — Regional License Dashboard (Plotly)
# Expects CSV at ../운전면허.csv (pages 폴더에서 한 단계 위).
# If not found, will also try '/mnt/data/운전면허.csv' (uploaded file path).

import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="운전면허 지역 통계", layout="wide")
st.title("운전면허 지역 통계 대시보드")
st.markdown("사이드바에서 작업을 선택하면 지역별(행정구) 통계를 표시합니다. CSV 파일이 상위 폴더에 있어야 합니다.")

# --- Sidebar ---
st.sidebar.header("설정")
task_labels = ["면허발급", "재발급", "적성검사", "면허갱신"]
selected_label = st.sidebar.selectbox("작업 선택", task_labels)

# prefer ../운전면허.csv (pages -> 상위), fallback to /mnt/data/운전면허.csv
default_paths = [
    os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "운전면허.csv")),
    "/mnt/data/운전면허.csv",
    os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "license_data.csv")),  # fallback english name
]

def find_csv(paths):
    for p in paths:
        try:
            if os.path.exists(p):
                return p
        except Exception:
            continue
    return None

csv_path = find_csv(default_paths)

if csv_path is None:
    st.error(
        "CSV 파일을 찾을 수 없습니다. 프로젝트 루트(상위 폴더)에 `운전면허.csv`를 두거나, "
        "Streamlit Cloud에 업로드 하세요. (예: pages 폴더에서 한 단계 위에 파일)"
    )
    st.info("샘플 컬럼 형식: Region(또는 지역), LicenseType(또는 작업/구분), Count(또는 건수)")
    st.stop()

st.caption(f"CSV 파일 경로: `{csv_path}`")

@st.cache_data
def load_and_normalize(path):
    df = pd.read_csv(path)
    # 표준 컬럼 찾기 (유연하게 매핑)
    cols = {c.lower(): c for c in df.columns}

    def find_col(key_options):
        for k in key_options:
            for clow, corig in cols.items():
                if k in clow:
                    return corig
        return None

    region_col = find_col(["region", "지역", "구", "행정구", "area", "district"])
    type_col = find_col(["type", "작업", "분류", "처리", "license", "업무"])
    count_col = find_col(["count", "건수", "수", "cnt", "건"])

    if region_col is None or type_col is None or count_col is None:
        # give more helpful message by returning dataframe plus None markers
        return df, region_col, type_col, count_col

    # ensure count is numeric
    df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)

    return df, region_col, type_col, count_col

df, region_col, type_col, count_col = load_and_normalize(csv_path)

if region_col is None or type_col is None or count_col is None:
    st.error(
        "CSV에서 필요한 컬럼을 자동으로 찾지 못했습니다.\n"
        "다음 컬럼 중 하나 이름을 포함하는 컬럼이 필요합니다:\n"
        "- 지역: 'Region', '지역', '구', '행정구' 등\n"
        "- 작업/구분: 'LicenseType', '작업', '분류', '처리' 등\n"
        "- 건수: 'Count', '건수', '수' 등\n\n"
        f"현재 파일의 컬럼: {list(df.columns)}"
    )
    st.stop()

# normalize values in type_col so we can match korean/english variants
def normalize_type_val(v):
    if pd.isna(v):
        return ""
    s = str(v).strip().lower()
    # common korean variants -> canonical labels
    if any(k in s for k in ["발급", "면허발급", "issuance"]):
        return "면허발급"
    if any(k in s for k in ["재발급", "reissu", "re-issu", "reissue"]):
        return "재발급"
    if any(k in s for k in ["적성", "적성검사", "aptitude", "test"]):
        return "적성검사"
    if any(k in s for k in ["갱신", "면허갱신", "renewal"]):
        return "면허갱신"
    # fallback: match exact words
    mapping = {
        "issuance": "면허발급",
        "reissue": "재발급",
        "aptitude": "적성검사",
        "renewal": "면허갱신"
    }
    return mapping.get(s, str(v).strip())

df["_norm_type"] = df[type_col].apply(normalize_type_val)
df["_region"] = df[region_col].astype(str).str.strip()
df["_count"] = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)

# Filter by selected_label
filtered = df[df["_norm_type"] == selected_label].copy()

if filtered.empty:
    st.warning(f"선택한 작업({selected_label})에 해당하는 데이터가 없습니다.")
    st.markdown("CSV에 어떤 작업들이 들어있는지 확인하려면 아래에서 전체 작업값 목록을 확인하세요.")
    st.write("파일에 존재하는 작업 값들(정규화된 값):", sorted(df["_norm_type"].unique()))
    st.stop()

# Aggregate by region
agg = filtered.groupby("_region", as_index=False)["_count"].sum().rename(columns={"_region":"Region","_count":"Count"})
agg = agg.sort_values("Count", ascending=False).reset_index(drop=True)

# build colors: first = red, others gray gradient
colors = []
n = len(agg)
for i in range(n):
    if i == 0:
        colors.append("rgba(220,20,60,1)")  # crimson
    else:
        # gray with opacity decreasing as rank increases
        # opacity range: 0.9 -> 0.2
        if n == 1:
            opacity = 0.9
        else:
            opacity = 0.9 - (i-1) * (0.7 / max(1, n-1))
            opacity = max(0.15, opacity)
        colors.append(f"rgba(120,120,120,{round(opacity, 3)})")

# Create Plotly bar chart
fig = px.bar(
    agg,
    x="Region",
    y="Count",
    text="Count",
    title=f"{selected_label} — 지역별 통계 (총 {agg['Count'].sum()}건)",
)

fig.update_traces(marker_color=colors, textposition="outside")
fig.update_layout(
    xaxis_title="행정구(Region)",
    yaxis_title="건수(Count)",
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    margin=dict(l=40, r=40, t=80, b=120),
    template="plotly_white",
)

# Show chart and table
st.plotly_chart(fig, use_container_width=True)

with st.expander("원본 집계 데이터 보기/다운로드"):
    st.dataframe(agg.style.format({"Count":"{:,}"}))
    csv_bytes = agg.to_csv(index=False).encode("utf-8-sig")
    st.download_button("CSV 다운로드", csv_bytes, file_name=f"{selected_label}_by_region.csv", mime="text/csv")

st.caption("※ CSV 파일이 프로젝트 루트(상위 폴더)에 있어야 자동으로 로드됩니다. 업로드된 파일은 `/mnt/data/운전면허.csv` 경로에서도 자동으로 시도합니다.")

