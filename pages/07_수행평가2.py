import streamlit as st
import pandas as pd
import plotly.express as px

st.title("서울시 여름철 평균기온 - 위도/경도별 정렬 시각화")

# CSV 경로 (상위 폴더)
CSV_PATH = "../서울시 여름철 평균기온 위치정보 (1998~2009년) (좌표계_ WGS1984).csv"

# 데이터 불러오기 함수
def load_data():
    # 먼저 로컬 경로 시도
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        if df.empty:
            raise pd.errors.EmptyDataError
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.warning("로컬 CSV 파일을 찾을 수 없거나 비어있습니다. 파일을 업로드해주세요.")
        uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except:
                df = pd.read_csv(uploaded_file, encoding="cp949")
            if df.empty:
                st.error("업로드한 CSV 파일이 비어 있습니다. 다른 파일을 선택해주세요.")
                return pd.DataFrame()
            return df
        else:
            return pd.DataFrame()  # 빈 데이터 반환

data = load_data()

# 데이터 없으면 종료
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

# Plotly 지도 시각화
if "latitude" in data.columns and "longitude" in data.columns:
    fig = px.scatter_mapbox(
        sorted_data,
        lat="latitude",
        lon="longitude",
        color=sorted_data.columns[2] if len(sorted_data.columns) > 2 else None,  # 임의 컬럼 선택
        hover_name=sorted_data.columns[0],
        zoom=10,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig)
