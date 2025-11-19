import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 여름철 평균기온", layout="wide")
st.title("서울시 여름철 평균기온 - 위도/경도별 순서 시각화")

# CSV 경로 (상위 폴더)
CSV_PATH = "../서울시 여름철 평균기온 위치정보 (1998~2009년) (좌표계_ WGS1984).csv"

# 데이터 불러오기
def load_data():
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
        if df.empty:
            raise pd.errors.EmptyDataError
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.warning("CSV 파일이 없거나 비어있습니다. 파일을 업로드해주세요.")
        uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except:
                df = pd.read_csv(uploaded_file, encoding="cp949")
            if df.empty:
                st.error("업로드한 CSV 파일이 비어 있습니다. 종료합니다.")
                return pd.DataFrame()
            return df
        else:
            return pd.DataFrame()

data = load_data()

# 데이터 없으면 종료
if data.empty:
    st.stop()

# 사용자 선택: 위도 or 경도
option = st.selectbox("정렬 기준을 선택하세요", ["위도", "경도"])
sort_col = "latitude" if option == "위도" else "longitude"

# 기온 컬럼명 자동 추정 (예: temperature, avg_temp 등)
temp_col = None
for col in data.columns:
    if "기온" in col or "temp" in col.lower():
        temp_col = col
        break
if temp_col is None:
    st.error("CSV에 기온 관련 컬럼이 없습니다.")
    st.stop()

# 정렬
sorted_data = data.sort_values(by=sort_col, ascending=True).reset_index(drop=True)

# 색상 그라데이션
num_rows = len(sorted_data)
colors = ["red"] + ["rgba(128,128,128," + f"{0.8*(1 - i/(num_rows-1))}" + ")" for i in range(1, num_rows)]

# Plotly 막대그래프
fig = go.Figure(go.Bar(
    x=sorted_data[temp_col],
    y=sorted_data[sort_col],
    orientation='h',
    marker_color=colors,
    text=sorted_data[temp_col],
    textposition='auto'
))

fig.update_layout(
    title=f"{option} 순으로 정렬된 기온",
    xaxis_title="기온",
    yaxis_title=option,
    yaxis=dict(autorange="reversed"),
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
