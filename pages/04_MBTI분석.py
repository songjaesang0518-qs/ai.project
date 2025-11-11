import streamlit as st
import pandas as pd
import plotly.express as px

# 📂 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 🌍 제목
st.title("🌎 세계 각국의 MBTI 유형 비율 시각화")
st.markdown("국가를 선택하면 해당 국가의 **MBTI 16유형 분포**를 볼 수 있습니다.")

# 🏳️ 국가 선택
countries = df["Country"].unique()
selected_country = st.selectbox("국가를 선택하세요", sorted(countries))

# 선택한 국가 데이터 가져오기
country_data = df[df["Country"] == selected_country].iloc[0, 1:]  # 첫 행, MBTI 열만 선택
country_df = pd.DataFrame({
    "MBTI": country_data.index,
    "비율": country_data.values
}).sort_values("비율", ascending=False)

# 🎨 색상 설정: 1등은 빨강, 나머지는 파랑 그라데이션
colors = ["#FF4C4C"] + px.colors.sequential.Blues[len(country_df) - 1]

# 📊 Plotly 막대그래프
fig = px.bar(
    country_df,
    x="MBTI",
    y="비율",
    color=country_df["비율"].rank(ascending=False),
    color_continuous_scale=["#FF4C4C"] + px.colors.sequential.Blues,
    title=f"{selected_country}의 MBTI 비율 분포",
)

fig.update_traces(
    hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}",
    marker=dict(line=dict(color="white", width=1))
)
fig.update_layout(
    coloraxis_showscale=False,
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=20
)

# 📈 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터도 표로 보기
with st.expander("📋 데이터 보기"):
    st.dataframe(country_df.reset_index(drop=True))
