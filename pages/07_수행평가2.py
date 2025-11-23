import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 관측소 기온 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌡️ 서울 관측소 위치 기반 평균 기온 분석")
st.markdown("---")

# 2. 데이터 로드 (경로 및 인코딩 수정)
@st.cache_data
def load_data(file_path):
    # 인코딩 오류 방지 로직 (cp949 -> euc-kr 순)
    encodings = ['cp949', 'euc-kr', 'utf-8']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding) 
            return df
        except Exception:
            continue
    
    # 모든 인코딩 실패 시
    st.error(f"데이터 로딩 중 치명적인 인코딩/경로 오류 발생.")
    st.error(f"파일 경로: '{file_path}'를 확인하거나, 파일 인코딩을 확인해주세요.")
    return pd.DataFrame()

data_df = load_data("temperature.csv")

if not data_df.empty:
    # 3. 데이터 전처리
    data_df['평균기온'] = pd.to_numeric(data_df['평균기온'], errors='coerce')
    data_df = data_df.dropna(subset=['위도', '경도', '평균기온']).reset_index(drop=True)

    # 4. 사용자 입력: 위도 또는 경도 선택
    st.sidebar.header("📊 그래프 옵션 선택")
    
    dimension_options = {
        "위도": "위도", 
        "경도": "경도"
    }
    selected_dimension_korean = st.sidebar.radio(
        "X축 기준(정렬 기준)을 선택하세요:",
        list(dimension_options.keys())
    )
    selected_dimension_col = dimension_options[selected_dimension_korean]

    # 5. 데이터 정렬 및 X축 레이블 생성
    sorted_df = data_df.sort_values(by='평균기온', ascending=False).reset_index(drop=True)
    num_stations = len(sorted_df)

    # **X축 레이블 생성**: '관측소명 (순위)' 형식으로 만들고, X축으로 사용할 별도의 컬럼 생성
    sorted_df['순위'] = sorted_df.index + 1
    sorted_df['X_Axis_Label'] = sorted_df['관측소명'] + " (" + sorted_df['순위'].astype(str) + "위)"

    # **색상 구현**: 1등은 빨간색, 나머지는 회색 그라데이션
    colors = ['#FF0000']  # 1등: Red

    if num_stations > 1:
        # 2등부터 마지막까지 회색 그라데이션 생성 (진한 회색 -> 옅은 회색)
        gray_values = np.linspace(0.75, 0.4, num_stations - 1)
        for val in gray_values:
            hex_val = f'#{int(val * 255):02x}{int(val * 255):02x}{int(val * 255):02x}'
            colors.append(hex_val)

    sorted_df['Color'] = colors[:num_stations]

    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        sorted_df, 
        # X축을 새로 만든 'X_Axis_Label' 컬럼으로 지정 -> 막대 아래에 지역명과 순위 표시됨
        x='X_Axis_Label', 
        y='평균기온', 
        hover_data=['관측소명', '주소', '평균기온', selected_dimension_col], 
        color='Color',
        color_discrete_map="identity",
        title=f"평균 기온 순위별 시각화 (정렬 기준: {selected_dimension_korean})",
        height=600
    )

    # 7. 레이아웃 및 디자인 조정
    fig.update_layout(
        xaxis_title="관측소명 (순위)", # X축 제목 변경
        yaxis_title="평균 기온 (°C)",
        showlegend=False, 
        hovermode="closest",
        # X축 레이블이 겹치지 않도록 기울이기
        xaxis={
            'categoryorder': 'array', 
            'categoryarray': sorted_df['X_Axis_Label'].tolist(),
            'tickangle': -45
        }
    )
    
    # 막대 위 텍스트(textposition)는 제거하여, 지역 정보가 X축에만 표시되도록 함
    fig.update_traces(
        textfont_size=11,
        marker_line_width=0
    )
    
    # 8. Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.error("데이터 로드에 실패했습니다. **위의 안내**를 참고하여 `temperature.csv`의 경로와 인코딩을 확인해주세요.")
