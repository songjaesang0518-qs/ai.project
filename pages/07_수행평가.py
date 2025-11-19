import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="운전면허 통계", layout="wide")

# CSV 경로 (pages 폴더 상위)
csv_path = os.path.join(os.path.dirname(__file__), "..", "운전면허.csv")

@st.cache_data
def load_data(path):
    # EUC-KR 인코딩으로 고정 (오류 방지)
    return pd.read_csv(path, encoding="euc-kr")

df = load_data(csv_path)

st.title("운전면허 통계 대시보드")

# 선택 옵션
type_options = ["면허발급", "재발급", "적성검사", "면허갱신"]

selected_type = st.selectbox("항목 선택", type_options)

# 지역 & 선택된 항목만 사용
plot_df = df[["구분", selected_type]].copy()
plot_df.columns = ["지역", "건수"]

# 내림차순 정렬
plot_df = plot_df.sort_values("건수", ascending=False)

# 색상 설정 (1등 빨강 → 나머지 회색 그라데이션)
colors = ["red"] + [
    f"rgba(150,150,150,{1 - i/len(plot_df)})" for i in range(1, len(plot_df))
]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=plot_df["지역"],
    y=plot_df["건수"],
    marker=dict(color=colors),
    hovertemplate="지역: %{x}<br>건수: %{y:,}건<extra></extra>"
))

fig.update_layout(
    title=f"{selected_type} 지역별 통계",
    xaxis_title="지역",
    yaxis_title="건수",
    template="plotly_white",
    height=650
)

st.plotly_chart(fig, use_container_width=True)
