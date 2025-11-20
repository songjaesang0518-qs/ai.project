import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 인기 음식점 분석", layout="wide")

st.title("📊 서울 관광 음식점 인기 순위 Dashboard")

# --------------------------
# CSV 로드 함수 (경로 오류 방지 + 인코딩 자동 처리)
# --------------------------
@st.cache_data
def load_data():
    path = "../seoul_food.csv"   # CSV는 상위 폴더
    try:
        return pd.read_csv(path, encoding="utf-8")
    except:
        return pd.read_csv(path, encoding="latin1")  # 가장 잘 읽힘

df = load_data()

if df is None:
    st.error("CSV 파일을 불러올 수 없습니다.")
    st.stop()

# --------------------------
# 깨진 컬럼명을 강제로 새 이름으로 교체 (오류 방지)
# --------------------------
df.columns = [
    "고유번호", "언어", "상호명", "컨텐츠URL", "주소",
    "상세주소", "전화번호", "웹사이트", "영업시간",
    "교통정보", "홈페이지언어", "메뉴"
]

# --------------------------
# 데이터 미리보기
# --------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# --------------------------
# 인기 순위 계산
# --------------------------
popular = df["상호명"].value_counts().reset_index()
popular.columns = ["상호명", "빈도수"]

# --------------------------
# 색상: 1등 빨간색 + 나머지 회색 그라데이션
# --------------------------
colors = ["red"]  # 1위 빨강

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
