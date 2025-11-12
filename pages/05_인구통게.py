import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import re
import os

# ----------------------------------------
# 한글 폰트 설정
# ----------------------------------------
# Streamlit Cloud 환경에서도 작동 가능하도록 폰트 다운로드
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

if not os.path.exists(font_path):
    import urllib.request
    os.makedirs(os.path.dirname(font_path), exist_ok=True)
    urllib.request.urlretrieve(
        "https://github.com/naver/nanumfont/blob/master/ttf/NanumGothic.ttf?raw=true",
        font_path,
    )

plt.rc("font", family=fm.FontProperties(fname=font_path).get_name())
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 깨짐 방지

# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    for col in df.columns[1:]:
        df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    return df

df = load_data()

# ----------------------------------------
# 앱 제목
# ----------------------------------------
st.title("🧑‍🤝‍🧑 서울시 행정구별 연령별 인구 시각화 (2025년 10월 기준)")
st.caption("행정구를 선택하면 연령별 인구수를 꺾은선 그래프로 보여줍니다.")

# ----------------------------------------
# 행정구 선택
# ----------------------------------------
region_list = df["행정구역"].tolist()
selected_region = st.selectbox("📍 행정구 선택", region_list)

region_data = df[df["행정구역"] == selected_region].iloc[0]

# ----------------------------------------
# 연령별 인구 컬럼 추출
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
# 그래프
# ----------------------------------------
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#f0f0f0")
ax.set_facecolor("#eaeaea")

ax.plot(ages, values, color="black", marker="o", linewidth=2)
ax.set_title(f"{selected_region} 연령별 인구수", fontsize=16, pad=15)
ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

ax.set_xticks(range(0, len(ages), 10))
ax.set_xticklabels([ages[i] for i in range(0, len(ages), 10)], rotation=45)

ymax = int(max(values)) + 100
ax.set_yticks(range(0, ymax, 100))

ax.grid(True, color="gray", alpha=0.3)

st.pyplot(fig)
