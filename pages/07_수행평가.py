# pages/region_license_dashboard.py
# Streamlit app — revised to avoid UnicodeDecodeError
# Attempts multiple encodings automatically.

import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="운전면허 지역 통계", layout="wide")
st.title("운전면허 지역 통계 대시보드 (Unicode-safe)")

# --- Sidebar ---
st.sidebar.header("설정")
license_tasks = ["면허발급", "재발급", "적성검사", "면허갱신"]
selected_task = st.sidebar.selectbox("작업 선택", license_tasks)

# Preferred search paths
SEARCH_PATHS = [
    os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "운전면허.csv")),
    "/mnt/data/운전면허.csv",
]

# Find CSV path
def find_csv(paths):
    for p in paths:
        try:
            if os.path.exists(p):
                return p
        except:
            pass
    return None

csv_path = find_csv(SEARCH_PATHS)
if csv_path is None:
    st.error("CSV 파일을 찾을 수 없습니다. 루트 폴더에 `운전면허.csv`를 배치하세요.")
    st.stop()

st.caption(f"CSV 파일 경로: `{csv_path}`")

# --- Safe CSV loader that avoids UnicodeDecodeError ---
def safe_read_csv(path):
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr", "latin1"]
    last_error = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc), enc
        except Exception as e:
            last_error = e
            continue
    raise last_error

# Load CSV
try:
    raw_df, used_enc = safe_read_csv(csv_path)
    st.caption(f"CSV 인코딩 자동 감지됨 → `{used_enc}`")
except Exception as e:
    st.error(f"CSV 파일을 여는 중 오류 발생: {e}")
    st.stop()

# --- Flexible column detection ---
cols = {c.lower(): c for c in raw_df.columns}

def find_col(keywords):
    for key in keywords:
        for low, orig in cols.items():
            if key in low:
                return orig
    return None

region_col = find_col(["region", "지역", "행정구", "구", "district", "area"])
type_col   = find_col(["type", "작업", "구분", "업무", "license", "분류"])
count_col  = find_col(["count", "건수", "숫자", "cnt", "수"])

if not all([region_col, type_col, count_col]):
    st.error("필수 컬럼을 자동으로 찾지 못했습니다. CSV 컬럼명을 확인하세요.")
    st.write("현재 CSV 컬럼:", list(raw_df.columns))
    st.stop()

# Clean DataFrame
df = raw_df.copy()
df[region_col] = df[region_col].astype(str).str.strip()
df[count_col]  = pd.to_numeric(df[count_col], errors="coerce").fillna(0).astype(int)

# Normalize type values
def normalize_task(v):
    if pd.isna(v): return ""
    s = str(v).lower().strip()
    if "발급" in s: return "면허발급"
    if "재발" in s or "reissu" in s: return "재발급"
    if "적성" in s or "aptitude" in s: return "적성검사"
    if "갱신" in s or "renew" in s: return "면허갱신"
    return s

df["_task"] = df[type_col].apply(normalize_task)

# Filter
df_filtered = df[df["_task"] == selected_task]
if df_filtered.empty:
    st.warning(f"'{selected_task}' 데이터가 없습니다.")
    st.write("CSV 내 작업 목록:", sorted(df["_task"].unique()))
    st.stop()

# Aggregate
agg = df_filtered.groupby(region_col)[count_col].sum().reset_index()
agg.columns = ["Region", "Count"]
agg = agg.sort_values("Count", ascending=False).reset_index(drop=True)

# Colors (red + gray gradient)
colors = []
N = len(agg)
for i in range(N):
    if i == 0:
        colors.append("rgba(220,20,60,1)")
    else:
        opacity = 0.9 - (i-1) * (0.65 / max(1, N-1))
        opacity = max(0.2, opacity)
        colors.append(f"rgba(120,120,120,{opacity})")

# Plot
title = f"{selected_task} — 지역별 건수 (총 {agg['Count'].sum()}건)"
fig = px.bar(agg, x="Region", y="Count", text="Count", title=title)
fig.update_traces(marker_color=colors, textposition="outside")
fig.update_layout(
    xaxis_title="지역",
    yaxis_title="건수",
    template="plotly_white",
    margin=dict(l=40, r=40, t=80, b=120)
)

st.plotly_chart(fig, use_container_width=True)

# Table download
with st.expander("데이터 보기/다운로드"):
    st.dataframe(agg)
    st.download_button(
        "CSV 다운로드",
        agg.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{selected_task}_집계.csv",
        mime="text/csv"
    )

# requirements.txt
# streamlit
# pandas
# plotly
