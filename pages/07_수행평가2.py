import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 인기 음식점 분석", layout="wide")

st.title("📊 서울 관광 음식점 인기 순위 Dashboard")

# --------------------------
# CSV 로드 함수
# --------------------------
@st.cache_data
def load_data():
    path = "../seoul_food.csv"   # CSV는 상위 폴더
    try:
        df = pd.read_csv(path, encoding="utf-8")
    except:
        df = pd.read_csv(path, encoding="cp949")
    return df

df = load_data()

if df is None:
    st.error("CSV 파일을 불러올 수 없습니다.")
    st.stop()

# --------------------------
# 데이터 미리보기
# --------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# --------------------------
# 인기 순위 계산
# --------------------------
# 상호명 컬럼 이름이 깨져서 들어오므로 자동으로 찾는 방식 사용
name_col = df.columns[df.columns.str.contains("상호|»óÈ£", regex=True)][0]

popular = df[name_col].value_counts().reset_index()
popular.columns = ["상호명", "빈도수"]

# --------------------------
# 색상: 1등 빨간색 + 나머지 회색 그라데이션
# --------------------------
colors = ["red"]  # 1위

total = len(popular)

for i in range(1, total):
    fade = int(200 + (55 / total) * i)  # 200~255 회색
    colors.append(f"rgb({fade}, {fade}, {fade})")

# --------------------------
# Plotly 그래프
# --------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=popular["상호명"],
        y=popular["빈도수"],
        marker=dict(color=colors),
        hovertemplate="<b>%{x}</b><br>언급 횟수: %{y}<extra></extra>"
    )
)

fig.update_layout(
    title="⭐ 서울시 인기 음식점 순위 (언급 빈도 기준)",
    xaxis_title="상호명",
    yaxis_title="언급 횟수",
    template="simple_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
