from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ 임베딩 모델 지정
embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta")
# 또는 jhgan/ko-sroberta-multitask, snunlp/kr-sbert 등으로 교체 가능

# ✅ FAISS 벡터 DB 로드
vectordb = FAISS.load_local(
    "faiss_store/contents",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# ✅ 질문 정규화 (필수)
import re
def normalize_query(query):
    patterns = [
        (r"(이|가|은|는)?\s?뭐야\??", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?뭔가요\??", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?뭐에요\??", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?무엇인가요\??", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?설명해줘", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?알려줘", "란 무엇인가요"),
        (r"(이|가|은|는)?\s?뜻은\?", "란 무엇인가요"),
    ]
    for pattern, repl in patterns:
        query = re.sub(pattern, repl, query)
    return query

# ✅ 테스트 질문
query = "귀어가 뭐야?"
normalized_query = normalize_query(query)

# ✅ 유사도 기반 검색
results = vectordb.similarity_search_with_score(normalized_query, k=5)

# ✅ 결과 출력
for i, (doc, score) in enumerate(results):
    print(f"\n[{i+1}] 유사도 점수: {score:.4f}")
    print("📄 파일:", doc.metadata.get("source"))
    print("📌 제목:", doc.metadata.get("title"))
    print("📎 내용 미리보기:\n", doc.page_content[:300])
    print("-" * 50)
