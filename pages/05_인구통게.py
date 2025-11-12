import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import os
import urllib.request

# ----------------------------------------
# ✅ 한글 폰트 자동 설정
# ----------------------------------------
def set_korean_font():
    font_dirs = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanumgothic/NanumGothic.ttf",
        "/usr/share/fonts/NanumGothic.ttf",
        "NanumGothic.ttf",
    ]
    for path in font_dirs:
        if os.path.exists(path):
            plt.rc("font", family=fm.FontProperties(fname=path).get_name())
            plt.rcParams["axes.unicode_minus"] = False
            return
    try:
        urllib.request.urlretrieve(
            "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true",
            "NanumGothic.ttf",
        )
        plt.rc("font", family=fm.FontProperties(fname="NanumGothic.ttf").get_name())
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        st.warning("⚠️ 한글 폰트를 불러오지 못했습니다. 영문만 표시될 수 있습니다.")

set_korean_font()

# ----------------------------------------
# ✅ 데이터 불러오기
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    for col in df.columns[1:]:
        df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    return df

df = load_data()

# ----------------------------------------
# ✅ 앱 제목
# ----------------------------------------
st.title("🧑‍🤝‍🧑 서울시 행정구별 인구 시각화 (2025년 10월 기준)")
st.caption("행정구별 연령별 및 연령대별 인구를 시각적으로 확인할 수 있습니다.")

# ----------------------------------------
# ✅ 탭 구성
# ----------------------------------------
tab1, tab2 = st.tabs(["📊 행정구별 연령별 인구 (꺾은선)", "🏙️ 연령대별 인구 TOP 구 (막대그래프)"])

# ---------------------------------------------------------------------
# 📊 탭 1: 행정구별 꺾은선 그래프
# ---------------------------------------------------------------------
with tab1:
    st.subheader("행정구별 연령별 인구 꺾은선 그래프")

    region_list = df["행정구역"].tolist()
    selected_region = st.selectbox("📍 행정구 선택", region_list)

    region_data = df[df["행정구역"] == selected_region].iloc[0]

    # 연령별 컬럼 감지
    age_pattern = re.compile(r"2025년10월_계_([\d~]+세|100세 이상)")
    age_cols = [col for col in df.columns if age_pattern.match(col)]

    ages = []
    values = []
    for col in age_cols:
        match = age_pattern.match(col)
        if match:
            ages.append(match.group(1))
            values.append(region_data[col])

    # 그래프
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#f0f0f0")
    ax.set_facecolor("#eaeaea")

    ax.plot(ages, values, color="black", marker="o", linewidth=2)
    ax.set_title(f"{selected_region} 연령별 인구수", fontsize=16, pad=15)
    ax.set_xlabel("나이", fontsize=12)
    ax.set_ylabel("인구수", fontsize=12)

    ax.set_xticks(range(0, len(ages), 2))
    ax.set_xticklabels([ages[i] for i in range(0, len(ages), 2)], rotation=45)

    ymax = int(max(values)) + 100
    ax.set_yticks(range(0, ymax, 100))
    ax.grid(True, color="gray", alpha=0.3)

    st.pyplot(fig)

# ---------------------------------------------------------------------
# 🏙️ 탭 2: 연령대별 인구 TOP 구 (막대그래프)
# ---------------------------------------------------------------------
with tab2:
    st.subheader("연령대별 인구 TOP 행정구")

    start_age = st.selectbox("🧍 시작 연령", list(range(0, 100, 10)), index=0)
    end_age = st.selectbox("👵 종료 연령", list(range(10, 101, 10)), index=9)

    if end_age <= start_age:
        st.warning("⚠️ 종료 연령은 시작 연령보다 커야 합니다.")
    else:
        # ✅ CSV 컬럼 이름에 숫자 범위를 자동으로 인식
        def get_age_range(col):
            nums = re.findall(r"\d+", col)
            return (int(nums[0]), int(nums[-1])) if nums else (None, None)

        selected_cols = []
        for col in df.columns:
            if "2025년10월_계_" in col:
                a1, a2 = get_age_range(col)
                if a1 is not None and (
                    (a1 >= start_age and a1 < end_age)
                    or (a2 >= start_age and a2 <= end_age)
                ):
                    selected_cols.append(col)

        if not selected_cols:
            st.error("⚠️ 선택한 연령대에 해당하는 데이터가 없습니다. CSV의 연령대 표기를 확인해주세요.")
        else:
            df["선택연령대_인구합계"] = df[selected_cols].sum(axis=1)
            df_sorted = df.sort_values("선택연령대_인구합계", ascending=False)

            # 그래프
            plt.style.use("default")
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor("#f0f0f0")
            ax.set_facecolor("#eaeaea")

            ax.bar(df_sorted["행정구역"], df_sorted["선택연령대_인구합계"], color="steelblue")
            ax.set_title(f"{start_age}세~{end_age}세 인구 많은 행정구", fontsize=16, pad=15)
            ax.set_xlabel("행정구", fontsize=12)
            ax.set_ylabel("인구수", fontsize=12)
            ax.set_yticks(range(0, int(df_sorted["선택연령대_인구합계"].max()) + 100, 100))
            ax.grid(True, axis="y", color="gray", alpha=0.3)
            plt.xticks(rotation=45)

            st.pyplot(fig)
