# build_faiss_vectorstore.py
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import os

def extract_and_save_faiss(base_dir="templates/contents", out_path="faiss_store/contents"):
    contentList = [] # 문서들의(contents 내의) 모든 chunk를 임시로 모으기

    # 텍스트 분할
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    # templates/contents 하위의 모든 html 파일 탐색
    for file_path in Path(base_dir).rglob("*.html"):
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 경로에서 폴더명과 파일명을 추출 (메타데이터용)
        folder = os.path.basename(os.path.dirname(file_path))
        page = os.path.splitext(os.path.basename(file_path))[0]

        # HTML 파싱
        soup = BeautifulSoup(html_content, 'html.parser')

        # # div name="section" 태그들 찾기 (conten_title이랑 content_text로 나눠놨음)
        sections = soup.select('[name="section"]')
        for section in sections:
            titles = section.select('[name="content_title"]')
            contents = section.select('[name="content_text"]')
            # 제목과 본문이 정확히 하나씩 있을 때만 처리 (1:1로 설정, 정확히 한 쌍일 때만 처리)
            if len(titles) == 1 and len(contents) == 1:
                title = titles[0].get_text(strip=True) # strip으로 태그 제거, 공백 제거
                content = contents[0].get_text(strip=True)
                # 본문을 chunk 단위로 나누기 -> 정밀도 높이기 위함(너무 길면 정확도 떨어짐..)
                chunks = splitter.split_text(content)
                for chunk in chunks:
                    # 각 조각을 리스트에 추가 (title, chunk 내용, 폴더, 파일명)
                    contentList.append([title, chunk, folder, page])

    # 데이터프레임으로 변환
    df = pd.DataFrame(contentList, columns=["title", "content", "folder", "page"])

    # LangChain Document 객체로 변환 (메타데이터 포함)
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


    # 임베딩 모델 LOAD
    embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    # FAISS 벡터 DB 생성
    vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
    vectorstore.save_local(out_path) # 지정 경로에 저장
    print(f"저장 완료: {len(documents)} chunks → {out_path}") # 완료 로그

# 스크립트 직접 실행 시 호출
if __name__ == "__main__":
    extract_and_save_faiss()
