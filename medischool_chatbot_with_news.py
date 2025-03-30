
import streamlit as st
import requests

# Hugging Face API 키 입력
hf_api_key = st.text_input("🔑 Hugging Face API 키를 입력하세요", type="password")
news_api_key = st.text_input("📰 NewsAPI 키를 입력하세요", type="password")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# 진단 데이터
disease_data = [
    {
        "질병": "감기",
        "증상": ["기침", "콧물", "두통", "목 아픔"],
        "체온조건": "36.5~37.5",
        "약품": ["없음", "생강차"],
        "행동": "따뜻한 물 마시기, 보건실에서 휴식"
    },
    {
        "질병": "독감",
        "증상": ["고열", "기침", "두통", "근육통", "오한"],
        "체온조건": "38 이상",
        "약품": ["타이레놀"],
        "행동": "조퇴, 병원 방문, 휴식, 충분한 수분 섭취"
    }
]

# 증상 리스트
all_symptoms = sorted(set(symptom for item in disease_data for symptom in item["증상"]))

# 진단 로직
def match_temp_condition(조건, 체온):
    if "이상" in 조건:
        기준 = float(''.join(filter(str.isdigit, 조건)))
        return 체온 >= 기준
    elif "~" in 조건:
        low, high = map(float, 조건.replace("℃", "").split("~"))
        return low <= 체온 <= high
    elif "정상" in 조건:
        return 36.0 <= 체온 <= 37.5
    elif "미열" in 조건:
        return 37.0 <= 체온 < 38.0
    elif "무관" in 조건 or "관계 없음" in 조건:
        return True
    return True

def diagnose(체온, 증상목록):
    for 항목 in disease_data:
        if match_temp_condition(항목["체온조건"], 체온):
            if any(증상 in 증상목록 for 증상 in 항목["증상"]):
                return 항목
    return {"질병": "알 수 없음", "약품": [], "행동": "보건실에 방문하여 상담을 받으세요."}

def ask_huggingface(prompt, hf_api_key):
    headers = {"Authorization": f"Bearer {hf_api_key}"}
    payload = {
        "inputs": f"사용자: {prompt}\nAI:",
        "parameters": {"temperature": 0.7, "max_new_tokens": 300}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].split("AI:")[-1].strip()
    else:
        return f"❌ 오류 발생: {response.text}"

# 뉴스 가져오기
def get_health_news(api_key):
    url = f"https://newsapi.org/v2/everything?q=질병 예방 OR 감염병&language=ko&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return []

# UI 시작
st.title("MediSchool (건강진단챗봇)")

menu = st.sidebar.selectbox("📚 메뉴 선택", ["건강 진단", "GPT 건강 질문", "건강 뉴스"])

if menu == "건강 진단":
    체온 = st.slider("🌡️ 현재 체온을 선택하세요", 35.0, 41.0, 36.8, 0.1)
    선택한_증상들 = st.multiselect("🤒 증상을 선택하세요", options=all_symptoms)
    if st.button("✅ 진단하기"):
        if 선택한_증상들:
            결과 = diagnose(체온, 선택한_증상들)
            st.subheader("🔍 진단 결과")
            st.write(f"• 질병: **{결과['질병']}**")
            st.write(f"• 추천 약품: {', '.join(결과['약품']) if 결과['약품'] else '없음'}")
            st.write(f"• 추천 행동: {결과['행동']}")
        else:
            st.warning("증상을 하나 이상 선택해주세요.")

elif menu == "GPT 건강 질문":
    질문 = st.text_input("💬 궁금한 건강 질문을 입력하세요")
    if st.button("💡 질문하기 (무료 GPT 사용)"):
        if 질문 and hf_api_key:
            with st.spinner("GPT가 답변 중입니다..."):
                답변 = ask_huggingface(질문, hf_api_key)
                st.success("GPT의 답변:")
                st.write(답변)
        elif not hf_api_key:
            st.error("❗ Hugging Face API 키를 입력해주세요.")

elif menu == "건강 뉴스":
    st.header("📰 최신 질병 관련 뉴스")
    if news_api_key:
        news = get_health_news(news_api_key)
        if news:
            for article in news[:5]:
                st.subheader(article["title"])
                st.write(article.get("description", ""))
                st.write(f"[기사 원문 보기]({article['url']})")
                if article.get("urlToImage"):
                    st.image(article["urlToImage"])
                st.markdown("---")
        else:
            st.warning("❗ 뉴스를 불러올 수 없습니다.")
    else:
        st.info("📰 NewsAPI 키를 입력해주세요.")
