import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="서울 인기 음식 그래프", layout="wide")

# --------------------------------------
# 🔥 CSV 불러오기 (상위 폴더)
# --------------------------------------
def load_data():
    # 현재 파일 위치 기준으로 CSV 경로 설정
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "..", "seoul_food.csv")

    return pd.read_csv(csv_path, encoding="utf-8")

df = load_data()

st.title("🍽 서울 관광 인기 음식 순위 시각화")
st.write("CSV 데이터 기반으로 인기 많은 순서대로 인터렉티브 그래프를 표시합니다.")

# --------------------------------------
# 🔥 인기 순 정렬
# --------------------------------------
df_sorted = df.sort_values(by="인기도", ascending=False).reset_index(drop=True)

# --------------------------------------
# 🔥 색상 설정 (1등=빨간색, 이후 회색 → 연한 회색 그라데이션)
# --------------------------------------
colors = ["red"] + [f"rgba(128,128,128,{0.9 - i*0.05})" for i in range(len(df_sorted)-1)]

# --------------------------------------
# 🔥 Plotly 막대 그래프
# --------------------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_sorted["음식명"],
        y=df_sorted["인기도"],
        marker=dict(color=colors)
    )
)

fig.update_layout(
    title="서울 인기 음식 순위",
    xaxis_title="음식명",
    yaxis_title="인기도",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
