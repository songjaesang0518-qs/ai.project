import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 경로 (상위 폴더)
CSV_PATH = "../서울시 여름철 평균기온 위치정보 (1998~2009년) (좌표계_ WGS1984).csv"

st.title("서울시 여름철 평균기온 - 위도/경도별 정렬 시각화")

# 데이터 불러오기
def load_data():
    try:
        return pd.read_csv(CSV_PATH, encoding="utf-8")
    except:
        return pd.read_csv(CSV_PATH, encoding="cp949")


data = load_data()

# 사용자 선택
option = st.selectbox("정렬 기준을 선택하세요", ["위도", "경도"])("정렬 기준을 선택하세요", ["latitude", "longitude"])

# 한국어 선택값을 실제 컬럼명으로 매핑
if option == "위도":
    sort_col = "latitude"
elif option == "경도":
    sort_col = "longitude"

# 정렬
sorted_data = data.sort_values(by=sort_col, ascending=True)
