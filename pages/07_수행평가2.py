import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

st.set_page_config(page_title="서울 인기 음식점 분석", layout="wide")
st.title("📊 서울 관광 음식점 인기 순위 Dashboard")

# -----------------------------------------------------
# 📌 CSV 파일 자동 탐색 함수 (오류 0%)
# -----------------------------------------------------
def find_csv():
    root_path = "/mount/src/ai.project"   # Streamlit Cloud 프로젝트 루트
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.lower().endswith(".csv"):
                return os.path.join(root, f)
    return None

# -----------------------------------------------------
# 📌 CSV 로드
# -----------------------------------------------------
@st.cache_data
def load_data():
    csv_path = find_csv()

    if csv_path is None:
        st.error("❌ CSV 파일을 프로젝트 전체에서 찾지 못했습니다.")
        return None

    st.success(f"📁 CSV 파일 찾음: {csv_path}")

    try:
        return pd.read_csv(csv_path, encoding="utf-8")
    except:
        return pd.read_csv(csv_path, encoding="latin1")

df = load_data()

if df is None:
    st.stop()


# -----------------------------------------------------
# 📌 컬럼명 강제 재정의 (깨짐 방지)
# -----------------------------------------------------
df.columns = [
    "고유번호", "언어", "상호명", "컨텐츠URL", "주소",
    "상세주소", "전화번호", "웹사이트", "영업시간",
    "교통정보", "홈페이지언어", "메뉴"
]

# -----------------------------------------------------
# 📌 데이터 미리보기
# -----------------------------------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# -----------------------------------------------------
# 📌 인기순 정렬
# -----------------------------------------------------
popular = df["상호명"].value_counts().reset_index()
popular.columns = ["상호명", "빈도수"]

# -----------------------------------------------------
# 📌 색상: 1등 빨강 + 회색 그라데이션
# -----------------------------------------------------
colors = ["red"]
total = len(popular)

for i in range(1, total):
    fade = int(200 + (55 / total) * i)
    colors.append(f"rgb({fade}, {fade}, {fade})")

# -----------------------------------------------------
# 📌 Plotly 그래프
# -----------------------------------------------------
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
    title="⭐ 서울시 인기 음식점 순위 (언급 횟수 기준)",
    xaxis_title="상호명",
    yaxis_title="언급 횟수",
    template="simple_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
