import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="서울 관측소 기온 분석",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌡️ 서울 관측소 위치 기반 평균 기온 분석")
st.markdown("---")

# 2. 데이터 로드 (상위 폴더에 있는 CSV 파일 로드)
@st.cache_data
def load_data(file_path):
    try:
        # Streamlit Cloud 환경에서 상위 폴더의 CSV 파일 경로
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except FileNotFoundError:
        st.error(f"Error: 파일을 찾을 수 없습니다. 경로를 확인해주세요: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
        return pd.DataFrame()

# Streamlit Cloud 배포를 가정하여 상위 폴더의 경로 지정
# 이 경로는 Streamlit Cloud에서 프로젝트 루트를 기준으로 함
data_df = load_data("../temperature.csv")

if not data_df.empty:
    # 3. 데이터 전처리
    # '평균기온' 컬럼을 숫자로 변환 (CSV에서 문자열로 읽혔을 경우 대비)
    data_df['평균기온'] = pd.to_numeric(data_df['평균기온'], errors='coerce')
    data_df = data_df.dropna(subset=['위도', '경도', '평균기온'])

    # 4. 사용자 입력: 경도 또는 위도 선택
    st.sidebar.header("📊 그래프 옵션 선택")
    
    dimension_options = {
        "위도": "위도", 
        "경도": "경도"
    }
    selected_dimension_korean = st.sidebar.radio(
        "정렬 기준을 선택하세요:",
        list(dimension_options.keys())
    )
    selected_dimension_col = dimension_options[selected_dimension_korean]

    st.sidebar.markdown("---")
    st.sidebar.info("기온이 높은 순서대로 관측소를 정렬하여 막대 그래프로 표시합니다.")

    # 5. 데이터 정렬 및 색상 지정
    # 평균 기온이 높은 순서대로 정렬
    sorted_df = data_df.sort_values(by='평균기온', ascending=False).reset_index(drop=True)
    
    # 색상 리스트 생성: 1등은 빨간색, 나머지는 회색 계열의 그라데이션
    num_stations = len(sorted_df)
    
    # Plotly의 Color Scales 사용: 'lightgrey'에서 'darkgrey'로 (1등 제외)
    # 1등은 빨간색 (red)
    colors = ['#FF0000']  # 1등: Red
    
    # 2등부터 마지막까지는 회색 그라데이션
    # Plotly는 HEX 코드를 사용하며, 회색 계열을 정의합니다.
    # 여기서는 간단하게 2등부터는 고정된 회색을 사용하고 시각적으로 1등을 강조합니다.
    # 더 복잡한 그라데이션은 Plotly의 color_continuous_scale 옵션으로 구현하는 것이 더 깔끔합니다.
    # 요청 사항에 맞춰 1등: 빨강, 나머지: 회색/흐려지는 느낌을 구현합니다.
    
    # 회색 그라데이션 (진한 회색 -> 옅은 회색)
    if num_stations > 1:
        gray_scale = ['#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3', '#E0E0E0'] # 예시 회색 계열
        # 관측소 수에 맞게 색상 리스트 채우기 (2등부터)
        for i in range(1, num_stations):
             # 2등부터는 옅은 회색으로 시작하는 느낌을 위해 반복
            colors.append(gray_scale[i % len(gray_scale)])
        
    # 데이터프레임에 색상 컬럼 추가
    sorted_df['Color'] = colors[:num_stations]


    # 6. Plotly 막대 그래프 생성
    fig = px.bar(
        sorted_df, 
        # x축: 선택된 위도/경도 값
        x=selected_dimension_col, 
        # y축: 평균 기온
        y='평균기온', 
        # 마우스 오버 시 표시할 텍스트
        hover_data=['관측소명', '주소'], 
        # 색상은 미리 지정한 Color 컬럼 사용
        color='Color',
        # 색상 값이 아닌 카테고리로 간주하여 색상을 명시적으로 매핑
        color_discrete_map="identity",
        # 그래프 제목
        title=f"평균 기온 상위 순위 ({selected_dimension_korean} 기준 기온 시각화)",
        # 막대 위 관측소명 표시
        text='관측소명',
        height=500
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
        xaxis={'categoryorder':'array', 'categoryarray': sorted_df[selected_dimension_col].tolist()}
    )
    
    # 텍스트 레이블(관측소명) 설정
    fig.update_traces(
        textposition='outside', 
        textfont_size=12,
        marker_line_width=0
    )

    # 8. Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
