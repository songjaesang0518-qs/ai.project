import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 여름철 평균기온", layout="wide")
st.title("서울시 여름철 평균기온 - 위도/경도별 순서 시각화")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # CSV 읽기
    try:
        data = pd.read_csv(uploaded_file, encoding="utf-8")
    except:
        data = pd.read_csv(uploaded_file, encoding="cp949")
    
    if data.empty:
        st.error("업로드한 CSV 파일이 비어 있습니다. 다른 파일을 선택해주세요.")
        st.stop()
    
    # 사용자 선택: 위도 or 경도
    option = st.selectbox("정렬 기준을 선택하세요", ["위도", "경도"])
    sort_col = "latitude" if option == "위도" else "longitude"

    # 기온 컬럼 자동 찾기
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

    # 색상 그라데이션: 1등 빨강, 나머지 흐려지는 회색
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

else:
    st.info("CSV 파일을 업로드해야 시각화가 가능합니다.")
