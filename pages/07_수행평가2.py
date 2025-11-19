import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 경로 (프로젝트 루트에 존재해야 함)
CSV_PATH = "서울시 여름철 평균기온 위치정보 (1998~2009년) (좌표계_ WGS1984).csv"

st.title("서울시 여름철 평균기온 - 위도/경도별 정렬 시각화")

# 데이터 불러오기
def load_data():
    try:
        return pd.read_csv(CSV_PATH, encoding="utf-8")
    except:
        return pd.read_csv(CSV_PATH, encoding="cp949")

data = load_data()

# 사용자 선택
option = st.selectbox("정렬 기준을 선택하세요", ["latitude", "longitude"])

# 정렬
sorted_data = data.sort_values(by=option, ascending=True)

# 색상: 1등=빨간색, 나머지 회색 그라데이션
colors = [
    "red" if i == 0 else f"rgba(150,150,150,{0.2 + 0.8*(i/len(sorted_data))})"
    for i in range(len(sorted_data))
]

# Plotly 그래프
fig = px.bar(
    sorted_data,
    x=option,
    y="temperature",
    title=f"{option} 기준 정렬된 기온 그래프",
)

fig.update_traces(marker_color=colors)
fig.update_layout(
    xaxis_title=option,
    yaxis_title="기온 (°C)",
)

st.plotly_chart(fig, use_container_width=True)
