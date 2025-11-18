# pages/subway_analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Subway Analysis", layout="wide")

# CSV 파일 불러오기 (상위 폴더)
csv_path = Path(__file__).resolve().parents[1] / "subway.csv"
df = pd.read_csv(csv_path, encoding="cp949")

# 컬럼명 정리
df.columns = ["date", "line", "station", "on", "off"]
df["total"] = df["on"] + df["off"]

# 날짜 선택 (2025년 10월만 필터링)
df["date"] = df["date"].astype(str)
oct2025 = df[df["date"].str.startswith("202510")]  # 2025년 10월

st.title("🚇 2025년 10월 지하철 승하차 분석")

# 날짜 선택 UI
dates = sorted(oct2025["date"].unique())
selected_date = st.selectbox("날짜 선택", dates)

# 호선 선택
lines = sorted(oct2025["line"].unique())
selected_line = st.selectbox("호선 선택", lines)

# 선택한 날짜 + 호선 필터링
filtered = oct2025[(oct2025["date"] == selected_date) & (oct2025["line"] == selected_line)]
filtered = filtered.sort_values("total", ascending=False)

# 색상 설정 (1등=빨강, 나머지=회색 그라데이션)
colors = ["red"] + [f"rgba(150,150,150,{0.9 - i*0.02})" for i in range(len(filtered)-1)]

# 막대그래프 생성
fig = go.Figure()
fig.add_trace(go.Bar(
    x=filtered["station"],
    y=filtered["total"],
    marker_color=colors,
))
fig.update_layout(
    title=f"{selected_date} • {selected_line} 승하차 총합 TOP 역",
    xaxis_title="역명",
    yaxis_title="승하차 총합",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

st.write("### 데이터 미리보기")
st.dataframe(filtered)
