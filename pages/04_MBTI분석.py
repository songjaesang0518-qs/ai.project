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
except Exception as e:
    st.error("❌ CSV 파일을 불러오지 못했습니다. 파일이 같은 폴더에 있는지 확인하세요.")
    st.stop()

# 🌍 제목
st.title("🌎 세계 각국의 MBTI 유형 비율 시각화")
st.markdown("국가를 선택하면 해당 국가의 **MBTI 16유형 비율**과 **MBTI 유형별 국가 비교 그래프**를 볼 수 있습니다.")

# 🏳️ 국가 선택
countries = sorted(df["Country"].unique().tolist())
selected_country = st.selectbox("국가를 선택하세요", countries)

# 선택한 국가 데이터
country_row = df[df["Country"] == selected_country]
if country_row.empty:
    st.warning(f"'{selected_country}' 데이터가 없습니다.")
    st.stop()

country_data = country_row.iloc[0, 1:]  # 첫 번째 행의 MBTI 비율 부분
country_df = pd.DataFrame({
    "MBTI": country_data.index,
    "비율": country_data.values
}).sort_values("비율", ascending=False).reset_index(drop=True)

# 🎨 색상: 1등 빨강, 나머지 파랑 계열
blues = px.colors.sequential.Blues[::-1]
colors = ["#FF4C4C"] + blues[:len(country_df) - 1]

# 📊 (1) 선택한 국가의 MBTI 비율 그래프
fig1 = px.bar(
    country_df,
    x="MBTI",
    y="비율",
    title=f"{selected_country}의 MBTI 비율 분포",
    text=country_df["비율"].apply(lambda x: f"{x*100:.1f}%")
)
fig1.update_traces(
    marker_color=colors,
    hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}",
    textposition="outside"
)
fig1.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    yaxis_tickformat=".0%",
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=22,
    showlegend=False
)
st.plotly_chart(fig1, use_container_width=True)

with st.expander("📄 데이터 보기"):
    st.dataframe(country_df)

# ------------------------------------------------------------------
# 📊 (2) MBTI 유형별 국가 순위 그래프
st.markdown("---")
st.header("🌐 MBTI 유형별 전 세계 국가 비교")

selected_mbti = st.selectbox("MBTI 유형을 선택하세요", [col for col in df.columns if col != "Country"])

# 해당 MBTI 기준으로 국가별 정렬
mbti_df = df[["Country", selected_mbti]].sort_values(selected_mbti, ascending=False).reset_index(drop=True)

# 상위 15개 + 한국/일본 추가 (중복 방지)
top_df = mbti_df.head(15)
extra_rows = mbti_df[mbti_df["Country"].isin(["South Korea", "Japan"])]

# 중복 제거 후 합치기
combined_df = pd.concat([top_df, extra_rows]).drop_duplicates(subset=["Country"]).reset_index(drop=True)

# 색상 지정 로직
def get_color(row):
    if row["Country"] == "South Korea":
        return "#1E90FF"  # 파랑
    elif row["Country"] == "Japan":
        return "#FF4C4C"  # 빨강
    elif row.name == 0:
        return "#FFD700"  # 1등 노랑
    else:
        return "#D3D3D3"  # 회색

combined_df["color"] = combined_df.apply(get_color, axis=1)

# 📈 (상위 15 + 한국/일본) 가로 막대 그래프
fig2 = px.bar(
    combined_df,
    x=selected_mbti,
    y="Country",
    orientation="h",
    title=f"{selected_mbti} 유형이 많은 국가 순위 (상위 15 + 🇰🇷🇯🇵 포함)",
    text=combined_df[selected_mbti].apply(lambda x: f"{x*100:.1f}%")
)
fig2.update_traces(
    marker_color=combined_df["color"],
    hovertemplate="국가: %{y}<br>비율: %{x:.2%}",
    textposition="outside"
)
fig2.update_layout(
    xaxis_title=f"{selected_mbti} 비율",
    yaxis_title="국가",
    yaxis={'categoryorder':'total ascending'},
    xaxis_tickformat=".0%",
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=22,
    showlegend=False,
    height=700
)
st.plotly_chart(fig2, use_container_width=True)
