import os
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS  # ✅ 최신 import
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings  # ✅ FAISS에 맞는 wrapper

def extract_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text()

def embed_all_html(template_dir="templates/contents"):
    raw_model = SentenceTransformer("all-MiniLM-L6-v2")
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    documents, texts = [], []

    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                text = extract_text_from_html(path)
                documents.append(Document(page_content=text, metadata={"source": path}))
                texts.append(text)

    embeddings = raw_model.encode(texts).tolist()
    text_embeddings = list(zip(texts, embeddings))

    db = FAISS.from_embeddings(text_embeddings, embedding=model)  # ✅ embedding 전달
    db.save_local("chatbot/vector_store")
    print(f"✅ {len(documents)}개 HTML 임베딩 완료")

if __name__ == "__main__":
    embed_all_html()

