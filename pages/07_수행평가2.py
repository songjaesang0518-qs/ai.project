import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="서울 인기 음식 그래프", layout="wide")

# --------------------------------------
# 🔥 CSV 읽기 (여러 인코딩 자동 시도)
# --------------------------------------
def load_data():
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "..", "seoul_food.csv")

    encodings = ["utf-8", "cp949", "euc-kr", "utf-8-sig"]

    for enc in encodings:
        try:
            return pd.read_csv(csv_path, encoding=enc)
        except UnicodeDecodeError:
            pass  # 다음 인코딩 시도

    st.error("❌ CSV 파일 인코딩을 읽을 수 없습니다. UTF-8 또는 CP949로 저장해주세요.")
    st.stop()


# --------------------------------------
# 🔥 데이터 로드
# --------------------------------------
df = load_data()

st.title("🍽 서울 관광 인기 음식 순위 시각화")
st.write("CSV 데이터 기반 인기 순위 그래프입니다.")

# 반드시 필요한 컬럼 확인
required_cols = ["음식명", "인기도"]
if not all(col in df.columns for col in required_cols):
    st.error("❌ CSV 파일에 '음식명' 또는 '인기도' 컬럼이 없습니다.")
    st.stop()

# --------------------------------------
# 🔥 인기 순 정렬
# --------------------------------------
df_sorted = df.sort_values(by="인기도", ascending=False).reset_index(drop=True)

# --------------------------------------
# 🔥 색상 (1등 빨간색 → 회색 그라데이션)
# --------------------------------------
colors = ["red"] + [
    f"rgba(128,128,128,{0.9 - i * 0.05})"
    for i in range(len(df_sorted) - 1)
]

# --------------------------------------
# 🔥 Plotly 그래프
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
