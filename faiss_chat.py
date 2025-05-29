from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import os

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
retriever = vectordb.as_retriever(search_kwargs={"k": 5})

# 프롬프트 템플릿 정의
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 귀어귀촌을 하는 사람들을 도와줄 유용한 정보를 제공하는 전문 챗봇입니다.

다음은 참고해야 할 문서 내용입니다:
----------------
{context}
----------------

위 내용을 바탕으로 사용자의 질문에 다음 방식으로 응답하세요:
1. 구조적이고 깔끔하고 간결하게 요약합니다.
2. 너무 긴 문장 대신 짧은 문장으로 씁니다.
3. 단계가 있는 경우 구분을 제외하고 간략하게 설명합니다.
4. 말을 예쁘고 부드럽게 마무리합니다.
5. 말끝 마무리 인삿말(예: 편안한 하루 되세요)은 생략하세요.
6. 오직 질문에 대한 핵심 정보만 전달하세요.

질문: {question}
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
    chain_type_kwargs={"prompt": prompt_template}
)

# 챗 응답 처리 함수
def get_chat_response(query):
    result = qa_chain.invoke({"query": query})

    answer = result["result"]
    sources = result.get("source_documents", [])

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
    test_query = "귀어는 뭔가요?"
    result = get_chat_response(test_query)

    print("문서 source들:")
    for s in result["sources"]:
        print(" →", s)

    print("\n응답 내용:\n", result["response"])
