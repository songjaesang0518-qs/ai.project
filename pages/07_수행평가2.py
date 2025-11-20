import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 음식점 인기순위", layout="wide")

st.title("📊 서울시 관광 음식점 인기 순위 분석")

# CSV 로드
@st.cache_data
def load_data():
    path = "../서울시 관광 음식.csv"   # 상위 폴더
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except:
        df = pd.read_csv(path, encoding="cp949")
    return df

df = load_data()

st.subheader("데이터 미리보기")
st.dataframe(df.head())

# 인기 기준: 상호명 등장 횟수(언어별 중복 중 가장 많이 언급된 음식점 = 인기)
popular = df["»óÈ£¸í"].value_counts().reset_index()
popular.columns = ["상호명", "빈도수"]

# 색상 지정: 1등 빨간색, 나머지는 회색 → 점점 흐려지는 그라데이션
colors = ["red"]  # 1위
total = len(popular)

for i in range(1, total):
    fade = int(200 + (55 / total) * i)  # 200~255 사이 밝아지는 회색
    colors.append(f"rgb({fade}, {fade}, {fade})")

# Plotly
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=popular["상호명"],
        y=popular["빈도수"],
        marker=dict(color=colors),
        hovertemplate="<b>%{x}</b><br>횟수: %{y}<extra></extra>"
    )
)

fig.update_layout(
    title="⭐ 인기 많은 음식점 순위 (언급 빈도 기준)",
    xaxis_title="상호명",
    yaxis_title="등장 횟수",
    template="simple_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

