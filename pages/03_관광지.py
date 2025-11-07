
# Streamlit app: Seoul Top10 tourist spots (Folium map)
# Save this file as `streamlit_app.py` and deploy to Streamlit Cloud.
# The requirements.txt content is included at the bottom of this file (after the triple dashes).

import streamlit as st
import folium
from streamlit_folium import st_folium
import io
import json

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

st.title("🌏 외국인들이 좋아하는 서울 주요 관광지 Top 10 — Folium 지도")
st.markdown("간단한 설명과 마커를 클릭하면 장소 설명을 볼 수 있어요. 스트림릿 클라우드에 그대로 업로드하면 작동합니다.")

# Top10 places (name, lat, lon, short description)
PLACES = [
    {"name": "Gyeongbokgung Palace (경복궁)", "lat": 37.579617, "lon": 126.977041, "desc": "Joseon 왕조의 대표 궁궐 — 역사와 건축을 한눈에."},
    {"name": "Changdeokgung & Secret Garden (창덕궁)", "lat": 37.582604, "lon": 126.991044, "desc": "궁궐과 비원(후원)의 아름다운 조화."},
    {"name": "Bukchon Hanok Village (북촌 한옥마을)", "lat": 37.582490, "lon": 126.984962, "desc": "한옥 골목에서 전통 가옥을 체험할 수 있어요."},
    {"name": "Insadong (인사동)", "lat": 37.574044, "lon": 126.986374, "desc": "한국 공예, 찻집, 기념품 상점이 모인 문화거리."},
    {"name": "Myeongdong (명동)", "lat": 37.560098, "lon": 126.986979, "desc": "쇼핑과 스트리트푸드를 즐기기 좋은 번화가."},
    {"name": "N Seoul Tower / Namsan (남산서울타워)", "lat": 37.551169, "lon": 126.988227, "desc": "서울 전망을 한눈에 — 케이블카와 전망대."},
    {"name": "Hongdae (홍대)", "lat": 37.556264, "lon": 126.922255, "desc": "젊음의 문화, 거리공연, 카페와 클럽의 중심지."},
    {"name": "Dongdaemun Design Plaza (DDP) (동대문)", "lat": 37.566295, "lon": 127.009340, "desc": "현대 건축과 야간 쇼핑의 명소."},
    {"name": "COEX / Gangnam (코엑스 · 강남)", "lat": 37.511100, "lon": 127.059684, "desc": "대형 쇼핑몰·아쿠아리움·컨벤션이 모여 있는 곳."},
    {"name": "Lotte World Tower / Seokchon Lake (롯데월드타워)", "lat": 37.513103, "lon": 127.102538, "desc": "초고층 전망대와 몰, 호수 공원의 조합."},
]

# Sidebar controls
st.sidebar.header("지도 설정")
initial_zoom = st.sidebar.slider("초기 확대 레벨", min_value=10, max_value=16, value=12)
center_choice = st.sidebar.selectbox("지도 중심 위치 선택", ["Seoul Center", "Gyeongbokgung", "Gangnam (COEX)"])
show_list = st.sidebar.checkbox("장소 목록 표시", value=True)

# Determine center coordinates
if center_choice == "Seoul Center":
    center_lat, center_lon = 37.5665, 126.9780
elif center_choice == "Gyeongbokgung":
    center_lat, center_lon = 37.579617, 126.977041
else:
    center_lat, center_lon = 37.511100, 127.059684

# Create folium map
m = folium.Map(location=[center_lat, center_lon], zoom_start=initial_zoom)

# Add markers
for p in PLACES:
    popup_html = f"<b>{p['name']}</b><br>{p['desc']}"
    folium.Marker(location=[p['lat'], p['lon']], popup=popup_html, tooltip=p['name']).add_to(m)

# Optional: draw lines connecting places (tour path)
if st.sidebar.checkbox("관광 루트 선 연결", value=False):
    coords = [[p['lat'], p['lon']] for p in PLACES]
    folium.PolyLine(coords, weight=3, opacity=0.6).add_to(m)

# Render map
st.subheader("지도 (클릭하면 설명 보기)")
st_folium(m, width=900, height=600)

# Show list of places
if show_list:
    st.subheader("Top 10 장소 목록")
    for i, p in enumerate(PLACES, start=1):
        st.markdown(f"**{i}. {p['name']}** — {p['desc']}")

# Provide downloadable requirements.txt content
requirements = """streamlit
folium
streamlit-folium
pandas
"""

st.sidebar.download_button("requirements.txt 다운로드", data=requirements, file_name="requirements.txt", mime="text/plain")

st.info("앱 파일명: streamlit_app.py — 스트림릿 클라우드에 업로드 하고 requirements.txt를 함께 넣으면 바로 작동합니다.")

# --- 아래는 requirements.txt 내용(복사해서 따로 파일로 만드셔도 됩니다) ---
# requirements.txt
# streamlit
# folium
# streamlit-folium
# pandas
