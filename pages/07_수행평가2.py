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

# 2. 데이터 로드 (경로 수정: 'temperature.csv'로 단순화)
@st.cache_data
def load_data(file_path):
    try:
        # **경로 수정**: 최상위 폴더에 파일이 있을 경우 'temperature.csv'로 접근합니다.
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except FileNotFoundError:
        st.error(f"⚠️ **파일 경로 오류!** `temperature.csv` 파일이 앱의 **최상위 폴더**에 있는지 확인해주세요. 현재 시도한 경로: `{file_path}`")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
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
        "정렬 기준 축을 선택하세요:",
        list(dimension_options.keys())
    )
    selected_dimension_col = dimension_options[selected_dimension_korean]

    st.sidebar.markdown("---")
    st.sidebar.info("평균 기온이 높은 순서대로 관측소를 정렬하여 시각화합니다.")

    # 5. 데이터 정렬 및 색상 지정
    # 평균 기온이 높은 순서대로 정렬
    sorted_df = data_df.sort_values(by='평균기온', ascending=False).reset_index(drop=True)
    num_stations = len(sorted_df)

    # 요청 사항: 1등은 빨간색, 나머지는 회색 그라데이션
    colors = ['#FF0000']  # 1등: Red

    if num_stations > 1:
        # 2등부터 마지막까지 부드러운 회색 그라데이션 생성
        # NumPy의 linspace를 사용하여 0.8 (진한 회색)에서 0.3 (옅은 회색)까지 균일하게 만듭니다.
        # r, g, b 값이 동일하면 회색이 됩니다.
        gray_values = np.linspace(0.8, 0.3, num_stations - 1)
        
        for val in gray_values:
            # RGB 값을 0-255 범위의 16진수 코드로 변환
            hex_val = f'#{int(val * 255):02x}{int(val * 255):02x}{int(val * 255):02x}'
            colors.append(hex_val)

    # 데이터프레임에 색상 컬럼 추가
    sorted_df['Color'] = colors[:num_stations]
    
    # 순위를 텍스트로 표시하기 위해 순위 컬럼 추가
    sorted_df['순위'] = sorted_df.index + 1

    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        sorted_df, 
        # x축: 선택된 위도/경도 값
        x=selected_dimension_col, 
        # y축: 평균 기온
        y='평균기온', 
        # 마우스 오버 시 표시할 텍스트
        hover_data=['관측소명', '주소', '평균기온', '순위'], 
        # 색상은 미리 지정한 Color 컬럼 사용
        color='Color',
        # 색상 값이 아닌 카테고리로 간주하여 색상을 명시적으로 매핑
        color_discrete_map="identity",
        # 그래프 제목
        title=f"평균 기온 상위 순위 ({selected_dimension_korean}을 기준으로 정렬)",
        # 막대 위 관측소명 표시
        text='관측소명',
        height=600
    )

    # 7. 레이아웃 및 디자인 조정
    fig.update_layout(
        xaxis_title=selected_dimension_korean,
        yaxis_title="평균 기온 (°C)",
        # 범례 숨기기 (색상은 순위 강조용이므로)
        showlegend=False, 
        # 툴팁 정보 표시 설정
        hovermode="x unified",
        # x축 정렬 순서를 'Color'에 의해 정해진 대로 유지 (기온 높은 순)
        # x축을 '관측소명'으로 설정하고, '평균기온' 기준으로 정렬하는 것이 더 직관적일 수 있으나
        # 요청에 따라 '위도/경도'를 x축에 유지하고 기온 순서로 정렬합니다.
        xaxis={
            'categoryorder': 'array', 
            'categoryarray': sorted_df[selected_dimension_col].tolist(),
            'tickangle': -45 # x축 레이블 기울이기
        }
    )
    
    # 텍스트 레이블(관측소명) 설정
    fig.update_traces(
        textposition='outside', 
        textfont_size=11,
        marker_line_width=0,
        text=sorted_df['관측소명'] + " (" + (sorted_df.index + 1).astype(str) + "위)"
    )

    # 8. Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
    
else:
    # 데이터 로드에 실패했을 경우, 사용자에게 조치 방법 안내
    st.error("데이터 로드에 실패했습니다. 다음 사항을 확인해주세요:")
    st.markdown("- `temperature.csv` 파일이 **최상위 폴더(루트)**에 위치하는지 확인")
    st.markdown("- 파일명과 코드에 사용된 파일명이 일치하는지 확인 (`temperature.csv`)")
