import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기", page_icon="🎯", layout="centered")

MBTI_OPTIONS = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# MBTI별 진로 추천 + 학과 + 성격 + 연봉
RECOMMENDATIONS = {
    "ISTJ": [
        {
            "career": "회계사 / 재무분석가",
            "majors": "회계학, 경영학, 경제학",
            "personality": "규칙을 잘 지키고 꼼꼼하며 책임감이 강해요.",
            "salary": "연봉 약 4,000만~7,000만 원 💰"
        },
        {
            "career": "공무원 / 행정직",
            "majors": "행정학, 법학, 경영학",
            "personality": "꾸준히 준비할 수 있고 절차를 중시하는 성향이에요.",
            "salary": "연봉 약 3,500만~6,000만 원 💼"
        }
    ],
    "ISFJ": [
        {
            "career": "간호사 / 보건의료인",
            "majors": "간호학, 보건학",
            "personality": "세심하고 책임감 강한 타입이에요. 사람을 돕는 걸 좋아해요.",
            "salary": "연봉 약 3,500만~6,000만 원 💊"
        },
        {
            "career": "초등교사 / 특수교사",
            "majors": "교육학, 아동학, 특수교육",
            "personality": "인내심 있고 안정적인 관계를 잘 만들어가요.",
            "salary": "연봉 약 4,000만~6,500만 원 🧑‍🏫"
        }
    ],
    "INFJ": [
        {
            "career": "상담심리사 / 임상심리사",
            "majors": "심리학, 상담학",
            "personality": "공감 능력이 뛰어나고 사람 마음을 잘 이해해요.",
            "salary": "연봉 약 3,500만~6,000만 원 🧠"
        },
        {
            "career": "사회복지사 / NGO 활동가",
            "majors": "사회복지학, 사회학",
            "personality": "가치 지향적이고 약자를 돕는 일에 보람을 느껴요.",
            "salary": "연봉 약 3,000만~5,000만 원 🤝"
        }
    ],
    "INTJ": [
        {
            "career": "연구원 / 데이터 과학자",
            "majors": "수학, 통계학, 컴퓨터공학",
            "personality": "분석적이고 전략적으로 사고해요.",
            "salary": "연봉 약 5,000만~9,000만 원 💻"
        },
        {
            "career": "경영 컨설턴트 / 기획자",
            "majors": "경영학, 산업공학",
            "personality": "장기적 계획과 체계적인 사고를 좋아해요.",
            "salary": "연봉 약 5,000만~10,000만 원 📊"
        }
    ],
    "ISTP": [
        {
            "career": "기계공학자 / 기술자",
            "majors": "기계공학, 전기공학",
            "personality": "현장 감각이 좋고 직접 해결하는 걸 선호해요.",
            "salary": "연봉 약 4,000만~8,000만 원 ⚙️"
        },
        {
            "career": "파일럿 / 항공정비사",
            "majors": "항공운항학, 항공공학",
            "personality": "즉흥적이지만 집중력이 뛰어나요.",
            "salary": "연봉 약 6,000만~1억 원 ✈️"
        }
    ],
    "ISFP": [
        {
            "career": "디자이너 / 시각예술가",
            "majors": "시각디자인, 예술대학",
            "personality": "감각이 뛰어나고 표현력이 좋아요.",
            "salary": "연봉 약 3,000만~6,000만 원 🎨"
        },
        {
            "career": "요리사 / 바리스타",
            "majors": "조리학, 호텔외식경영",
            "personality": "실용적이고 현장에서 빛나는 스타일이에요.",
            "salary": "연봉 약 3,000만~5,000만 원 ☕"
        }
    ],
    "INFP": [
        {
            "career": "작가 / 편집자",
            "majors": "국어국문학, 문예창작, 미디어학",
            "personality": "표현력이 뛰어나고 감성이 풍부해요.",
            "salary": "연봉 약 3,000만~5,500만 원 ✍️"
        },
        {
            "career": "예술치료사 / 창작예술가",
            "majors": "미술치료, 음악치료, 예술계열",
            "personality": "감성적이고 치유적인 활동에 소질이 있어요.",
            "salary": "연봉 약 3,500만~6,000만 원 🎵"
        }
    ],
    "INTP": [
        {
            "career": "소프트웨어 개발자 / 연구개발",
            "majors": "컴퓨터공학, 수학",
            "personality": "논리적이고 아이디어 탐구를 즐겨요.",
            "salary": "연봉 약 5,000만~9,000만 원 💻"
        },
        {
            "career": "학자 / 이론연구자",
            "majors": "자연과학, 인문학",
            "personality": "깊이 있는 사고를 즐기며 분석을 잘해요.",
            "salary": "연봉 약 4,000만~7,000만 원 📚"
        }
    ],
    "ENFP": [
        {
            "career": "창업가 / 스타트업 실무자",
            "majors": "경영학, 창업학, 디자인씽킹",
            "personality": "아이디어가 풍부하고 모험을 즐겨요.",
            "salary": "연봉 약 4,000만~1억 원 🚀"
        },
        {
            "career": "홍보(PR) / 콘텐츠 크리에이터",
            "majors": "미디어학, 커뮤니케이션",
            "personality": "창의적이고 트렌드에 민감해요.",
            "salary": "연봉 약 3,000만~7,000만 원 📱"
        }
    ],
    "ENTP": [
        {
            "career": "전략기획 / 컨설팅",
            "majors": "경영학, 경제학, 산업공학",
            "personality": "아이디어를 빠르게 실행하는 혁신가예요.",
            "salary": "연봉 약 5,000만~10,000만 원 💼"
        },
        {
            "career": "변호사 / 정치분야 전문가",
            "majors": "법학, 정치외교",
            "personality": "논리적이고 설득력이 강해요.",
            "salary": "연봉 약 6,000만~1억 원 ⚖️"
        }
    ],
    "ESTJ": [
        {
            "career": "사업관리자 / 운영매니저",
            "majors": "경영학, 산업경영",
            "personality": "실용적이고 책임감이 강해요.",
            "salary": "연봉 약 4,000만~8,000만 원 🧾"
        },
        {
            "career": "경찰 / 소방관",
            "majors": "경찰행정학, 소방안전",
            "personality": "규율과 신뢰를 중요시해요.",
            "salary": "연봉 약 3,500만~6,500만 원 🚓"
        }
    ],
    "ESFJ": [
        {
            "career": "간호사 / 보건행정",
            "majors": "간호학, 보건행정",
            "personality": "사람을 챙기고 관계를 중시해요.",
            "salary": "연봉 약 3,500만~6,000만 원 💉"
        },
        {
            "career": "인사(HR) / 고객관리",
            "majors": "경영학, 심리학",
            "personality": "소통 능력이 뛰어나고 팀 분위기를 잘 만들어요.",
            "salary": "연봉 약 4,000만~7,000만 원 🗂️"
        }
    ],
    "ENFJ": [
        {
            "career": "교사 / 교육기획자",
            "majors": "교육학, 상담학",
            "personality": "사람을 이끌고 동기부여를 잘해요.",
            "salary": "연봉 약 4,000만~7,000만 원 📘"
        },
        {
            "career": "HR 컨설턴트 / 코치",
            "majors": "심리학, 경영학",
            "personality": "타인의 성장을 돕는 걸 좋아해요.",
            "salary": "연봉 약 4,500만~8,000만 원 👥"
        }
    ],
    "ENTJ": [
        {
            "career": "CEO / 사업가",
            "majors": "경영학, 경제학",
            "personality": "리더십과 추진력이 매우 강해요.",
            "salary": "연봉 약 8,000만~1억 이상 💼"
        },
        {
            "career": "투자분석가 / 컨설턴트",
            "majors": "경영학, 금융학, 경제학",
            "personality": "전략적으로 큰 그림을 잘 봐요.",
            "salary": "연봉 약 6,000만~1억 원 📈"
        }
    ],
}

st.title("MBTI로 보는 맞춤형 진로 추천 🎯")
st.markdown("청소년도 보기 쉽게! 네 MBTI를 선택하면 어울리는 진로와 예상 연봉을 알려줄게 😄")

choice = st.selectbox("당신의 MBTI를 선택하세요", options=["선택 안함"] + MBTI_OPTIONS)

if choice != "선택 안함":
    recs = RECOMMENDATIONS.get(choice)
    if recs:
        st.markdown(f"## {choice}형에게 어울리는 진로 ✨")
        for i, r in enumerate(recs, 1):
            st.markdown(f"### {i}. {r['career']}")
            st.markdown(f"- **적합 학과:** {r['majors']}")
            st.markdown(f"- **어울리는 성격:** {r['personality']}")
            st.markdown(f"- **예상 연봉:** {r['salary']}")
            st.write("---")
        st.info("💡 참고: MBTI는 참고용이에요! 진짜 진로는 너의 흥미, 경험, 가치관을 함께 고려하길 추천해요.")
    else:
        st.error("이 MBTI에 대한 정보가 아직 없어요 😢")
else:
    st.write("👉 MBTI를 선택하면 관련 진로와 연봉 정보를 보여줄게요!")
    
st.caption("Made with ❤️ by ChatGPT — 교육용 예시입니다.")
