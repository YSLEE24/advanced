from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def load_faiss_index(index_dir="vector_store/contents"):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
        db = FAISS.load_local(index_dir, embeddings=embedding_model)
        return db
    except Exception as e:
        print("예외발생: ", e)

    

# 사용 예시
if __name__ == "__main__":
    db = load_faiss_index()
    
    query = "이 서비스의 목적이 뭐야?"
    docs = db.similarity_search(query, k=3)
    
    for i, doc in enumerate(docs, start=1):
        print(f"\n[{i}] 🔎 Source: {doc.metadata['source']}")
        print(doc.page_content[:300], "...")
