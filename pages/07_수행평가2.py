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
    try:
        # **인코딩 수정**: 'cp949' 또는 'euc-kr'을 시도하여 한글 인코딩 오류 해결
        # 'temperature.csv'로 경로를 단순화하여 파일 경로 오류 해결
        df = pd.read_csv(file_path, encoding='cp949') 
        return df
    except Exception as e:
        # cp949로 실패하면 euc-kr로 재시도
        try:
            df = pd.read_csv(file_path, encoding='euc-kr')
            return df
        except Exception:
            st.error(f"데이터 로딩 중 치명적인 인코딩/경로 오류 발생.")
            st.error(f"파일 경로: '{file_path}'를 확인하거나, 파일 인코딩을 'utf-8', 'cp949', 'euc-kr' 중 하나로 변경해보세요.")
            st.error(f"원인 오류: {e}")
            return pd.DataFrame()

# Streamlit Cloud 배포를 가정하여 최상위 폴더의 경로 지정
data_df = load_data("temperature.csv")

if not data_df.empty:
    # 3. 데이터 전처리
    # '평균기온' 컬럼을 숫자로 변환하고 결측치 제거
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

    st.sidebar.markdown("---")
    st.sidebar.info("평균 기온이 높은 순서대로 관측소를 정렬하여 시각화합니다. 1위는 빨간색으로 강조됩니다.")

    # 5. 데이터 정렬 및 색상 지정
    # 평균 기온이 높은 순서대로 정렬
    sorted_df = data_df.sort_values(by='평균기온', ascending=False).reset_index(drop=True)
    num_stations = len(sorted_df)

    # **색상 구현**: 1등은 빨간색, 나머지는 회색 그라데이션 (어둡게 -> 흐리게)
    colors = ['#FF0000']  # 1등: Red

    if num_stations > 1:
        # 2등부터 마지막까지 회색 그라데이션 생성 (0.75: 진한 회색, 0.4: 옅은 회색)
        # RGB 값을 0-255 범위의 16진수 코드로 변환하여 부드러운 그라데이션 구현
        gray_values = np.linspace(0.75, 0.4, num_stations - 1)
        
        for val in gray_values:
            hex_val = f'#{int(val * 255):02x}{int(val * 255):02x}{int(val * 255):02x}'
            colors.append(hex_val)

    # 데이터프레임에 색상 컬럼 추가
    sorted_df['Color'] = colors[:num_stations]
    
    # 텍스트 레이블에 순위를 포함하기 위해 순위 컬럼 추가
    sorted_df['순위'] = sorted_df.index + 1
    sorted_df['Label'] = sorted_df['관측소명'] + " (" + (sorted_df.index + 1).astype(str) + "위)"

    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        sorted_df, 
        # X축을 선택된 위도/경도 값으로 설정
        x=selected_dimension_col, 
        y='평균기온', 
        hover_data=['관측소명', '주소', '평균기온'], 
        # 미리 지정한 'Color' 컬럼을 사용하고, 색상 매핑을 'identity'로 설정
        color='Color',
        color_discrete_map="identity",
        title=f"평균 기온 순위별 시각화 ({selected_dimension_korean} 기준)",
        height=600
    )

    # 7. 레이아웃 및 디자인 조정
    fig.update_layout(
        xaxis_title=selected_dimension_korean,
        yaxis_title="평균 기온 (°C)",
        showlegend=False, 
        hovermode="closest",
        # X축을 기온 순서대로 정렬하기 위해 categoryorder 사용
        xaxis={
            'categoryorder': 'array', 
            'categoryarray': sorted_df[selected_dimension_col].tolist(),
            'tickangle': -45 # X축 레이블 기울이기
        }
    )
    
    # 텍스트 레이블(관측소명 + 순위) 설정
    fig.update_traces(
        textposition='outside', 
        textfont_size=11,
        marker_line_width=0,
        text=sorted_df['Label']
    )
    
    # 8. Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
    
else:
    # 데이터 로드 실패 시 안내 메시지
    st.error("데이터 로드에 실패했습니다. **위의 오류 메시지**를 참고하여 `temperature.csv`의 경로와 인코딩을 확인해주세요.")
