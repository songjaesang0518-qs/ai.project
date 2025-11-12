import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import os
import urllib.request

# ----------------------------------------
# ✅ 한글 폰트 자동 설정 (NanumGothic)
# ----------------------------------------
def set_korean_font():
    font_dirs = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanumgothic/NanumGothic.ttf",
        "/usr/share/fonts/NanumGothic.ttf",
        "NanumGothic.ttf",
    ]

    # 폰트가 이미 있으면 그걸 사용
    for path in font_dirs:
        if os.path.exists(path):
            plt.rc("font", family=fm.FontProperties(fname=path).get_name())
            plt.rcParams["axes.unicode_minus"] = False
            return

    # 없으면 직접 다운로드
    os.makedirs(os.path.dirname(font_dirs[0]), exist_ok=True)
    try:
        urllib.request.urlretrieve(
            "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true",
            font_dirs[0],
        )
        plt.rc("font", family=fm.FontProperties(fname=font_dirs[0]).get_name())
        plt.rcParams["axes.unicode_minus"] = False
    except Exception as e:
        st.warning("⚠️ 한글 폰트를 불러오지 못했습니다. 영문만 표시될 수 있습니다.")
        print("폰트 오류:", e)

set_korean_font()

# ----------------------------------------
# ✅ 데이터 불러오기
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    # 숫자 변환
    for col in df.columns[1:]:
        df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    return df

df = load_data()

# ----------------------------------------
# ✅ 앱 제목
# ----------------------------------------
st.title("🧑‍🤝‍🧑 서울시 행정구별 연령별 인구 시각화 (2025년 10월 기준)")
st.caption("행정구를 선택하면 연령별 인구수를 꺾은선 그래프로 보여줍니다.")

# ----------------------------------------
# ✅ 행정구 선택
# ----------------------------------------
region_list = df["행정구역"].tolist()
selected_region = st.selectbox("📍 행정구 선택", region_list)

region_data = df[df["행정구역"] == selected_region].iloc[0]

# ----------------------------------------
# ✅ 연령별 인구 데이터 추출
# ----------------------------------------
age_pattern = re.compile(r"2025년10월_계_(\d+세|100세 이상)")
age_cols = [col for col in df.columns if age_pattern.match(col)]

ages = []
values = []
for col in age_cols:
    match = age_pattern.match(col)
    if match:
        ages.append(match.group(1))
        values.append(region_data[col])

# ----------------------------------------
# ✅ 그래프
# ----------------------------------------
plt.style.use("default")
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#f0f0f0")
ax.set_facecolor("#eaeaea")

ax.plot(ages, values, color="black", marker="o", linewidth=2)
ax.set_title(f"{selected_region} 연령별 인구수", fontsize=16, pad=15)
ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

# X축 10살 단위
ax.set_xticks(range(0, len(ages), 10))
ax.set_xticklabels([ages[i] for i in range(0, len(ages), 10)], rotation=45)

# Y축 100명 단위
ymax = int(max(values)) + 100
ax.set_yticks(range(0, ymax, 100))

ax.grid(True, color="gray", alpha=0.3)
st.pyplot(fig)

