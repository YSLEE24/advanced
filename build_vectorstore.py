# ✅ build_faiss_vectorstore_section_only.py

from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import os

def extract_and_save_faiss(base_dir="templates/contents", out_path="faiss_store/contents"):
    contentList = []  # 전체 문서 chunk 담을 리스트

    # ✅ 텍스트 분할기: 600자 단위, 80자 겹치기
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "],
    )

    # ✅ 모든 HTML 파일 순회
    for file_path in Path(base_dir).rglob("*.[hH][tT][mM][lL]"):  # 대소문자 모두 인식
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        folder = os.path.basename(os.path.dirname(file_path))
        page = os.path.splitext(os.path.basename(file_path))[0]

        # ✅ BeautifulSoup 파싱
        soup = BeautifulSoup(html_content, 'html.parser')

        # ✅ 모든 section 추출
        sections = soup.select('[name="section"]')

        for section in sections:
            # ✅ title 추출 (없을 수도 있음)
            title_div = section.select_one('[name="content_title"]')
            title = title_div.get_text(strip=True) if title_div else ""

            # ✅ section 전체 텍스트 추출 (title + 본문 포함)
            section_text = section.get_text(separator="\n", strip=True)

            # ✅ chunk 단위 분리
            chunks = splitter.split_text(section_text)

            for chunk in chunks:
                contentList.append([title, chunk, folder, page])

    # ✅ DataFrame 변환
    df = pd.DataFrame(contentList, columns=["title", "content", "folder", "page"])

    # ✅ LangChain 문서 객체 변환
    documents = [
        Document(
            page_content=f"{row['title']}\n{row['page']}\n{row['content']}",
            metadata={
                "title": row['title'],
                "folder": row['folder'],
                "page": row['page'],
                "source": f"templates/contents/{row['folder']}/{row['page']}.html"
            }
        )
        for _, row in df.iterrows()
    ]

    # ✅ 임베딩 모델 로딩
    embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta-multitask")

    # ✅ 디버깅: 전체 문서 수 확인
    print(f"\n📌 전체 문서 개수: {len(set(df['page']))}개, 총 chunk 수: {len(documents)}개")

    # ✅ 벡터스토어 저장
    vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
    vectorstore.save_local(out_path)
    print(f"✅ 저장 완료: {out_path}")

# ✅ 스크립트 직접 실행 시
if __name__ == "__main__":
    extract_and_save_faiss()
