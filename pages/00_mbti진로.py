import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기", page_icon="🎯", layout="centered")

MBTI_OPTIONS = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
]

# 각 MBTI에 대해 2개의 진로 추천과 설명(적합 학과, 어울리는 성격)을 적어둠
RECOMMENDATIONS = {
    "ISTJ": [
        {
            "career": "회계사 / 재무분석가",
            "majors": "회계학, 경영학, 경제학",
            "personality": "규칙을 잘 지키고, 꼼꼼하며 책임감 있는 편. 숫자와 자료 정리에 강함."
        },
        {
            "career": "공무원 / 행정직",
            "majors": "행정학, 법학, 경영학",
            "personality": "체계적이고 꾸준히 준비할 수 있는 성격. 절차와 규정을 존중함."
        }
    ],
    "ISFJ": [
        {
            "career": "간호사 / 보건의료인",
            "majors": "간호학, 보건학, 임상의학 계열",
            "personality": "타인을 돕는 걸 좋아하고 책임감이 강함. 세심한 배려가 장점."
        },
        {
            "career": "초등교사 / 특수교사",
            "majors": "교육학, 아동학, 특수교육",
            "personality": "아이들과 안정적으로 관계를 맺는 데 강함. 인내심이 많음."
        }
    ],
    "INFJ": [
        {
            "career": "상담심리사 / 임상심리사",
            "majors": "심리학, 상담학",
            "personality": "사람의 마음에 관심이 많고 공감 능력이 뛰어남. 깊이 있는 통찰을 줌."
        },
        {
            "career": "사회복지사 / NGO 활동가",
            "majors": "사회복지학, 사회학, 국제학",
            "personality": "가치 지향적이고 도덕감이 강함. 약자를 돕는 데 동기부여됨."
        }
    ],
    "INTJ": [
        {
            "career": "연구원 / 데이터 과학자",
            "majors": "수학, 통계학, 컴퓨터공학, 전공 관련 이공계",
            "personality": "전략적이고 분석적. 복잡한 문제 해결을 즐김."
        },
        {
            "career": "경영 컨설턴트 / 기획자",
            "majors": "경영학, 산업공학, 경제학",
            "personality": "장기적 계획을 세우고 체계적으로 실행하는 유형."
        }
    ],
    "ISTP": [
        {
            "career": "기계공학자 / 기술자",
            "majors": "기계공학, 전기공학, 공학계열",
            "personality": "현장 감각이 좋고 손으로 만드는 걸 좋아함. 문제를 직접 해결하는 스타일."
        },
        {
            "career": "파일럿 / 항공정비사",
            "majors": "항공운항학, 항공공학",
            "personality": "즉흥적이면서도 집중력이 좋아 기술적 상황에서 강함."
        }
    ],
    "ISFP": [
        {
            "career": "디자이너 / 시각예술가",
            "majors": "시각디자인, 산업디자인, 예술대학",
            "personality": "감각이 뛰어나고 감정을 표현하는 걸 좋아함. 창의적이고 유연함."
        },
        {
            "career": "요리사 / 바리스타",
            "majors": "조리학, 호텔외식경영",
            "personality": "실용적이고 손으로 만드는 걸 좋아함. 현장에서 빛남."
        }
    ],
    "INFP": [
        {
            "career": "작가 / 편집자",
            "majors": "국어국문학, 문예창작, 미디어학",
            "personality": "내면이 풍부하고 표현력이 좋음. 가치와 의미를 중요시함."
        },
        {
            "career": "예술치료사 / 창작예술가",
            "majors": "미술치료, 음악치료, 예술계열",
            "personality": "감성적이고 치유적인 활동에 소질이 있음."
        }
    ],
    "INTP": [
        {
            "career": "소프트웨어 개발자 / 연구개발",
            "majors": "컴퓨터공학, 소프트웨어학, 수학",
            "personality": "논리적이고 호기심이 많음. 이론과 시스템에 관심이 많음."
        },
        {
            "career": "학자 / 이론연구자",
            "majors": "자연과학, 인문학 중 관심 분야",
            "personality": "깊게 사고하고 새로운 아이디어를 탐구하는 유형."
        }
    ],
    "ESTP": [
        {
            "career": "영업사원 / 마케팅 실무",
            "majors": "경영학, 마케팅, 광고학",
            "personality": "대인관계가 좋고 에너지가 넘침. 실전에서 능력을 발휘함."
        },
        {
            "career": "응급구조사 / 현장관리자",
            "majors": "응급구조학, 안전공학",
            "personality": "위기 상황에서 빠르게 판단하고 행동함. 현실적 해결사."
        }
    ],
    "ESFP": [
        {
            "career": "연예 / 공연예술",
            "majors": "연기학, 무대예술, 방송학",
            "personality": "사교적이고 무대에서 빛남. 사람들 앞에서 표현하는 걸 즐김."
        },
        {
            "career": "이벤트 플래너 / 관광서비스",
            "majors": "호텔관광학, 이벤트학",
            "personality": "현장 감각이 뛰어나고 사람들을 즐겁게 하는 데 소질 있음."
        }
    ],
    "ENFP": [
        {
            "career": "창업가 / 스타트업 실무",
            "majors": "경영학, 창업학, 디자인씽킹 관련 과",
            "personality": "아이디어가 풍부하고 사람을 끌어당기는 매력이 있음. 모험을 즐김."
        },
        {
            "career": "홍보(PR) / 콘텐츠 크리에이터",
            "majors": "미디어학, 커뮤니케이션",
            "personality": "창의적이고 사람들과 소통하는 데 능함. 트렌드에 민감함."
        }
    ],
    "ENTP": [
        {
            "career": "전략기획 / 컨설팅",
            "majors": "경영학, 경제학, 산업공학",
            "personality": "아이디어를 빠르게 만들어 실험하기 좋아함. 토론을 즐김."
        },
        {
            "career": "변호사 / 논리적 설득이 필요한 직업",
            "majors": "법학, 정치외교",
            "personality": "논리적이고 말로 설득하는 데 능숙함. 경쟁적 성향도 있음."
        }
    ],
    "ESTJ": [
        {
            "career": "사업관리자 / 운영매니저",
            "majors": "경영학, 산업경영",
            "personality": "조직을 운영하고 사람을 이끄는 데 강함. 실용적이고 책임감 있음."
        },
        {
            "career": "경찰 / 소방관",
            "majors": "경찰행정학, 소방안전",
            "personality": "규율을 중요시하고 위기대응에 강함. 신뢰받는 유형."
        }
    ],
    "ESFJ": [
        {
            "career": "간호사 / 보건행정",
            "majors": "간호학, 보건행정",
            "personality": "사람을 챙기고 관계를 중요시함. 팀워크에 강함."
        },
        {
            "career": "인사(HR) / 고객관리",
            "majors": "경영학, 심리학",
            "personality": "소통 능력이 좋고 조직의 분위기를 잘 관리함."
        }
    ],
    "ENFJ": [
        {
            "career": "교사 / 교육 기획자",
            "majors": "교육학, 상담학",
            "personality": "사람을 이끌고 동기부여하는 데 탁월함. 따뜻한 리더십 보유."
        },
        {
            "career": "HR 컨설턴트 / 코칭",
            "majors": "심리학, 경영학",
            "personality": "타인의 성장을 돕는 데 동기부여됨. 커뮤니케이션 뛰어남."
        }
    ],
    "ENTJ": [
        {
            "career": "CEO / 사업가",
            "majors": "경영학, 경제학, 산업공학",
            "personality": "리더십과 추진력이 뛰어나며 목표지향적임."
        },
        {
            "career": "전략 컨설턴트 / 투자분석가",
            "majors": "경영학, 금융학, 경제학",
            "personality": "전략적으로 큰 그림을 보고 빠르게 의사결정함."
        }
    ],
}

st.title("MBTI로 보는 맞춤형 진로 추천 🎯")
st.markdown("청소년도 편하게 볼 수 있게, 친근한 말투로 구성했어 — MBTI를 골라봐! 😄")

choice = st.selectbox("당신의 MBTI를 선택하세요", options=["선택 안함"] + MBTI_OPTIONS)

if choice and choice != "선택 안함":
    recs = RECOMMENDATIONS.get(choice)
    if recs:
        st.markdown(f"### {choice}형을 위한 추천 진로")
        for i, r in enumerate(recs, start=1):
            st.markdown(f"**{i}. {r['career']}** { '✨' if i==1 else '💡'}")
            st.markdown(f"- **어떤 학과가 적합할까?** {r['majors']}")
            st.markdown(f"- **어떤 성격이 어울릴까?** {r['personality']}")
            st.write("\n")

        st.info("참고: MBTI는 성향을 보여주는 도구일 뿐이에요. 실제 직업 선택은 관심사, 경험, 환경 등을 함께 고려하길 추천해요! 😊")
        st.write("---")
        st.markdown("원하면 다른 MBTI도 골라서 여러 옵션을 비교해봐~")
    else:
        st.error("해당 MBTI에 대한 추천이 준비되지 않았어요.")
else:
    st.write("MBTI를 선택하면 관련된 진로 추천을 보여줄게요 ✨")

st.caption("Made with ❤️ — 간단한 교육용 예시입니다.")
