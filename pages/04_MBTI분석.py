import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 국가별 분포", layout="wide")

# 📂 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'countriesMBTI_16types.csv' 파일이 같은 폴더에 없습니다.")
    st.stop()

# 🌍 제목
st.title("🌎 세계 각국의 MBTI 유형 비율 시각화")
st.markdown("국가를 선택하면 해당 국가의 **MBTI 16유형 비율**을 볼 수 있습니다.")

# 🏳️ 국가 선택
countries = df["Country"].unique().tolist()
selected_country = st.selectbox("국가를 선택하세요", sorted(countries))

# 선택한 국가 데이터 가져오기
country_row = df[df["Country"] == selected_country]
if country_row.empty:
    st.warning(f"'{selected_country}' 데이터가 없습니다.")
    st.stop()

country_data = country_row.iloc[0, 1:]  # MBTI 16유형만
country_df = pd.DataFrame({
    "MBTI": country_data.index,
    "비율": country_data.values
}).sort_values("비율", ascending=False).reset_index(drop=True)

# 🎨 색상: 1등은 빨강, 나머지는 파랑 그라데이션
blues = px.colors.sequential.Blues[::-1]
colors = ["#FF4C4C"] + blues[:len(country_df) - 1]

# 📊 그래프 생성
fig = px.bar(
    country_df,
    x="MBTI",
    y="비율",
    title=f"{selected_country}의 MBTI 비율 분포",
    text=country_df["비율"].apply(lambda x: f"{x*100:.1f}%")
)

fig.update_traces(
    marker_color=colors,
    hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}",
    textposition="outside"
)
fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    plot_bgcolor="white",
    paper_bgcolor=_
