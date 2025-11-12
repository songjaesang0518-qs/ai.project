import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------
# 데이터 불러오기
# ----------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv")
    # 숫자형 변환 (콤마 제거)
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

# 선택된 행정구 데이터 추출
region_data = df[df["행정구역"] == selected_region].iloc[0]

# ----------------------------------------
# 연령대별 인구 추출
# (열 이름 중 '2025년10월_계_'로 시작하고 '_세' 또는 '_세 이상'으로 끝나는 열만)
# ----------------------------------------
age_cols = [col for col in df.columns if "2025년10월_계_" in col and ("세" in col)]
ages = []
values = []

for col in age_cols:
    age_label = col.replace("2025년10월_계_", "")
    if "세 이상" in age_label:
        age_label = "100세 이상"
    ages.append(age_label)
    values.append(region_data[col])

# ----------------------------------------
# 그래프 그리기
# ----------------------------------------
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("#f0f0f0")  # 전체 배경색
ax.set_facecolor("#eaeaea")  # 그래프 내부 배경색

ax.plot(ages, values, color="black", marker="o", linewidth=2)
ax.set_title(f"{selected_region} 연령별 인구수", fontsize=16, pad=15)
ax.set_xlabel("나이", fontsize=12)
ax.set_ylabel("인구수", fontsize=12)

# x축: 10살 단위 구분선
ax.set_xticks(range(0, len(ages), 10))
ax.set_xticklabels([ages[i] for i in range(0, len(ages), 10)], rotation=45)

# y축: 100명 단위 구분선
ymax = int(max(values)) + 100
ax.set_yticks(range(0, ymax, 100))

ax.grid(True, color="gray", alpha=0.3)
st.pyplot(fig)
