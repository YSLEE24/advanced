from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS  # 최신 import

embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")

def get_answer(question: str) -> str:
    db = FAISS.load_local(
    "chatbot/vector_store/contents",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True  # 신뢰된 경우에만!
)
    docs = db.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    return f"""[어부바 챗봇의 답변]\n\n{context}"""
