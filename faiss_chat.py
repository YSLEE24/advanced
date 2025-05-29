from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import os
import re

# TensorFlow 자동 로딩 방지 (속도 개선)
os.environ["USE_TF"] = "0"

# 임베딩 모델 설정 (주의: model 인스턴스 넘기지 말고 model_name 사용)
embedding_model = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask"
)

# 저장된 FAISS 벡터 DB 로드
vectordb = FAISS.load_local(
    "faiss_store/contents",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Retriever 생성
retriever = vectordb.as_retriever(
    search_type="similarity",  # ✅ MMR 말고 단순 유사도 기반
    search_kwargs={"k": 4}
)

# 프롬프트 템플릿 정의
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    너는 어촌 정착, 귀어귀촌 지원에 대해 잘 아는 상담 챗봇이야.
    다음 문서들을 참고해서 '귀어'나 관련 정책에 대해 최대한 정확하고 간단히 알려줘.
    참고해야 할 문서에 없는 내용은 답하지마.

    참고 문서:
    {context}

    사용자 질문:
    {question}

    답변:
    """
)

# Google Gemini Flash 연결
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # "gemini-2.5-flash-preview-05-20",
    temperature=0.2,
    google_api_key="AIzaSyB0iXFU5Ocz_MkD8sJBe5wofGEhf2j3OCo"
)

# QA 체인 구성
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template},
    input_key="question"
)

# ✅ 질문 정규화 함수 추가 (기존 흐름 안 건드림)
def normalize_query(query):
    query = query.strip()
    
    # 구어체 서술형 종결 표현을 공식 표현으로 정규화
    replacements = {
        # 가장 일반적인 "뭐야", "뭐에요", "뭔가요" 계열
        r"(이|가)?\s*(뭐야|뭐임|머임|머야|뭐에요|뭐예요|뭐냐|뭐니|뭔가요|\?)$": "란 무엇인가요",
        
        # "모야", "모임", "머임", "머게", "모게" 등 오타/구어체도 흡수
        r"(이|가)?\s*(모야|모임|머게|모게|머임|머야)$": "란 무엇인가요",

        # "뭔데", "몬데", "뭐게", "뭐길래"도 대응
        r"(이|가)?\s*(뭔데|뭐게|뭐길래|몬데)$": "란 무엇인가요",

        # "뭐라", "뭐라고", "머라", "머라고"
        r"(이|가)?\s*(뭐라|뭐라고|머라|머라고)$": "란 무엇인가요",

        # "뜻이 뭐야", "뜻 알려줘", "무슨 뜻" 등
        r"(이|가)?\s*(뜻)?\s*(이)?\s*(뭐야|뭐에요|뭐임|머임|머야)?$": "란 무엇인가요",

        # "~에 대해 알려줘", "~설명해줘", "~궁금해", "~말해줘"
        r"(에 대해)?\s*(알려줘|설명해줘|궁금해|말해줘)$": "란 무엇인가요",
    }

    for pattern, replacement in replacements.items():
        if re.search(pattern, query):
            return re.sub(pattern, replacement, query)
    return query

# 챗 응답 처리 함수
def get_chat_response(query):
    # ✅ 정규화 로그 출력 (추가)
    print("[질문 원본]:", query)
    
    # ✅ 전처리 적용
    normalized_query = normalize_query(query)
    
    # ✅ 정규화 결과 확인
    print("[정규화된 질문]:", normalized_query)

    # 1. 유사도 점수 확인용
    docs_with_scores = vectordb.similarity_search_with_score(normalized_query, k=5)

    result = qa_chain.invoke({"question": normalized_query})

    answer = result["result"]
    sources = result.get("source_documents", [])

    # 3. 유사도 함께 보기
    for doc, score in docs_with_scores:
        print(f"[{doc.metadata.get('title')}] - 유사도 점수: {score:.4f}")
        print("내용 미리보기:", doc.page_content[:200])
        print("---")

    source_links = []

    for doc in sources:
        raw_path = doc.metadata.get("source", "")
        title = doc.metadata.get("title", "관련 문서")

        if isinstance(raw_path, str) and raw_path:
            try:
                clean_path = raw_path.replace("\\", "/")
                if clean_path.startswith("templates/contents/"):
                    relative_path = clean_path[len("templates/contents/"):]
                    folder, filename = relative_path.split("/", 1)
                    filename_no_ext = filename.rsplit(".", 1)[0]
                    page_link = f"/section/{folder}/{filename_no_ext}"

                    if not any(link["url"] == page_link for link in source_links):
                        source_links.append({
                            "url": page_link,
                            "title": title
                        })
            except Exception as e:
                print("링크 생성 실패:", e)
                continue

    return {
        "response": answer,
        "sources": source_links
    }

# 테스트용 실행
if __name__ == "__main__":
    test_query = "양식장 관련해서 알려줘"  # 원문 그대로
    result = get_chat_response(test_query)  # 내부에서 정규화되도록

    print("문서 source들:")
    for s in result["sources"]:
        print(" →", s)

    print("\n응답 내용:\n", result["response"])
