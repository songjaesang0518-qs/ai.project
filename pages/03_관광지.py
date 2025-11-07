# Streamlit app: Seoul Top10 tourist spots (Folium map with improved markers and subway info)
# Save this file as `streamlit_app.py` and deploy to Streamlit Cloud.
# The requirements.txt content is included at the bottom of this file.

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

st.title("🌏 외국인들이 좋아하는 서울 주요 관광지 Top 10 — Folium 지도")
st.markdown("지도 위 마커를 클릭하면 설명과 지하철역 정보를 볼 수 있어요. 관광지별 상세 이유도 아래에서 볼 수 있습니다.")

# Top10 places (name, lat, lon, description, nearest subway)
PLACES = [
    {"name": "Gyeongbokgung Palace (경복궁)", "lat": 37.579617, "lon": 126.977041, 
     "desc": "조선시대의 정궁으로, 한국 전통 건축미와 근정전, 경회루 등 대표 유적이 있는 곳.",
     "station": "경복궁역 (3호선)"},

    {"name": "Changdeokgung & Secret Garden (창덕궁)", "lat": 37.582604, "lon": 126.991044, 
     "desc": "유네스코 세계문화유산으로 지정된 궁궐. 자연과 조화를 이룬 비원(후원)이 특히 유명해요.",
     "station": "안국역 (3호선)"},

    {"name": "Bukchon Hanok Village (북촌 한옥마을)", "lat": 37.582490, "lon": 126.984962, 
     "desc": "서울 도심 속 전통 한옥이 잘 보존된 마을로, 인생샷 명소로도 인기!",
     "station": "안국역 (3호선)"},

    {"name": "Insadong (인사동)", "lat": 37.574044, "lon": 126.986374, 
     "desc": "전통 찻집, 공예품, 기념품이 즐비한 한국 문화거리로 외국인 관광객에게 인기 만점.",
     "station": "종각역 (1호선)"},

    {"name": "Myeongdong (명동)", "lat": 37.560098, "lon": 126.986979, 
     "desc": "서울의 대표 쇼핑거리! 화장품, 패션, 길거리 음식이 즐비한 번화가예요.",
     "station": "명동역 (4호선)"},

    {"name": "N Seoul Tower / Namsan (남산서울타워)", "lat": 37.551169, "lon": 126.988227, 
     "desc": "서울의 전망을 한눈에 볼 수 있는 명소로, 야경과 사랑의 자물쇠가 유명하죠.",
     "station": "명동역 (4호선)"},

    {"name": "Hongdae (홍대)", "lat": 37.556264, "lon": 126.922255, 
     "desc": "젊음과 예술의 거리로, 버스킹·클럽·카페가 가득한 핫플레이스!",
     "station": "홍대입구역 (2호선·경의중앙선·공항철도)"},

    {"name": "Dongdaemun Design Plaza (DDP) (동대문)", "lat": 37.566295, "lon": 127.009340, 
     "desc": "자하 하디드가 설계한 미래형 건축물! 야시장과 쇼핑몰이 인접해요.",
     "station": "동대문역사문화공원역 (2·4·5호선)"},

    {"name": "COEX / Gangnam (코엑스 · 강남)", "lat": 37.511100, "lon": 127.059684, 
     "desc": "대형 쇼핑몰, 아쿠아리움, 스타필드 도서관까지 한곳에서 즐길 수 있어요.",
     "station": "삼성역 (2호선)"},

    {"name": "Lotte World Tower / Seokchon Lake (롯데월드타워)", "lat": 37.513103, "lon": 127.102538, 
     "desc": "555m 초고층 타워! 전망대와 롯데월드몰, 석촌호수가 어우러진 명소입니다.",
     "station": "잠실역 (2·8호선)"},
]

# Sidebar controls
st.sidebar.header("🗺️ 지도 설정")
zoom = st.sidebar.slider("초기 확대 레벨", 10, 16, 12)
center_choice = st.sidebar.selectbox("지도 중심 위치 선택", ["Seoul Center", "Gyeongbokgung", "Gangnam (COEX)"])
show_route = st.sidebar.checkbox("관광 루트 선 연결", value=False)

if center_choice == "Seoul Center":
    center_lat, center_lon = 37.5665, 126.9780
elif center_choice == "Gyeongbokgung":
    center_lat, center_lon = 37.579617, 126.977041
else:
    center_lat, center_lon = 37.511100, 127.059684

# Folium map setup with better marker icons
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

for i, p in enumerate(PLACES, start=1):
    popup_html = f"""<b>{i}. {p['name']}</b><br>{p['desc']}<br><i>🚇 가장 가까운 역: {p['station']}</i>"""
    folium.Marker(
        location=[p['lat'], p['lon']],
        popup=popup_html,
        tooltip=p['name'],
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)

if show_route:
    coords = [[p['lat'], p['lon']] for p in PLACES]
    folium.PolyLine(coords, color="blue", weight=3, opacity=0.6).add_to(m)

st.subheader("📍 관광지 지도")
st_folium(m, width=900, height=600)

st.subheader("✨ 관광지별 상세 설명")
for i, p in enumerate(PLACES, start=1):
    st.markdown(f"**{i}. {p['name']}**  ")
    st.markdown(f"➡️ {p['desc']}  ")
    st.markdown(f"🚇 **가장 가까운 지하철역:** {p['station']}  ")
    st.markdown("---")

requirements = """streamlit
folium
streamlit-folium
pandas
"""

st.sidebar.download_button("requirements.txt 다운로드", data=requirements, file_name="requirements.txt", mime="text/plain")

st.info("이 코드를 `streamlit_app.py`로 저장하고 `requirements.txt`를 함께 업로드하면 스트림릿 클라우드에서 바로 실행됩니다.")

# --- requirements.txt ---
# streamlit
# folium
# streamlit-folium
# pandas
