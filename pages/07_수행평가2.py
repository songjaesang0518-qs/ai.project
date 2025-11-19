import streamlit as st
import pandas as pd
import plotly.express as px

st.title("서울시 여름철 평균기온 - 위도/경도별 정렬 시각화")

# CSV 경로 (상위 폴더)
CSV_PATH = "../서울시 여름철 평균기온 위치정보 (1998~2009년) (좌표계_ WGS1984).csv"

# 데이터 불러오기
def load_data():
    try:
        return pd.read_csv(CSV_PATH, encoding="utf-8")
    except FileNotFoundError:
        st.warning("CSV 파일을 찾을 수 없습니다. 파일을 업로드해주세요.")
        uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
        if uploaded_file is not None:
            try:
                return pd.read_csv(uploaded_file, encoding="utf-8")
            except:
                return pd.read_csv(uploaded_file, encoding="cp949")
        else:
            return pd.DataFrame()  # 빈 데이터프레임 반환

data = load_data()

# 데이터가 없으면 중단
if data.empty:
    st.stop()

# 사용자 선택
option = st.selectbox("정렬 기준을 선택하세요", ["위도", "경도"])

# 한국어 선택값을 실제 컬럼명으로 매핑
sort_col = "latitude" if option == "위도" else "longitude"

# 정렬
sorted_data = data.sort_values(by=sort_col, ascending=True)

# 정렬된 데이터 표시
st.dataframe(sorted_data)

# Plotly 시각화 예시
fig = px.scatter_mapbox(
    sorted_data,
    lat="latitude",
    lon="longitude",
    color="temperature",  # 컬럼명에 맞게 수정하세요
    size="temperature",
    hover_name="location",  # 컬럼명에 맞게 수정하세요
    zoom=10,
    mapbox_style="open-street-map"
)
st.plotly_chart(fig)
