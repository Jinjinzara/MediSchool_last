
# MediSchool 학생 건강 진단 챗봇 🩺📰

이 앱은 학생용 건강 진단 챗봇으로, 증상과 체온을 기반으로 간단한 질병을 진단하고  
무료 GPT에게 건강 관련 질문을 할 수 있으며, NewsAPI를 이용해 **최신 건강 뉴스**까지 확인할 수 있습니다.

## 주요 기능
- ✅ 증상 + 체온 기반 간단 건강 진단
- 🧠 Hugging Face 무료 GPT를 통한 건강 상담
- 📰 NewsAPI 연동 – 최신 한국어 건강 뉴스 표시

## 실행 방법

1. 필요한 라이브러리 설치
```bash
pip install -r requirements.txt
```

2. Streamlit 앱 실행
```bash
streamlit run medischool_chatbot_with_news.py
```

3. 실행된 웹 브라우저 창에서:
   - Hugging Face API 키 입력
   - NewsAPI 키 입력
   - 각 메뉴에서 기능 사용 가능

---

## API 키 발급 방법

- Hugging Face: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- NewsAPI: [https://newsapi.org](https://newsapi.org)

🔐 키는 보안상 공개하지 말고 개인적으로 보관해주세요.
