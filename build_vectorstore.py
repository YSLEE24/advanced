# build_faiss_vectorstore.py

from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import os
import ast

def extract_and_save_faiss(base_dir="templates/contents", out_path="faiss_store/contents"):
    contentList = []  # 문서 내의 모든 chunk를 모아 둘 리스트

    # ✅ 텍스트 분할기 설정: chunk는 600자, 80자 겹치기 (중복 문맥 보존)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n\n", "\n", ".", " "],
    )

    # ✅ templates/contents 하위의 모든 HTML 파일 탐색
    for file_path in Path(base_dir).rglob("*.html"):
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 메타데이터: 폴더명과 파일명 추출
        folder = os.path.basename(os.path.dirname(file_path))
        page = os.path.splitext(os.path.basename(file_path))[0]

        # ✅ 템플릿 탭 구조 처리: {% set tabs = [ ... ] %} 형태의 탭이 있는 경우
        import re

        if '{% set tabs = [' in html_content:
            try:
                # ✅ 정규식으로 모든 탭 블록 추출
                tabs_raw = re.findall(r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'''(.*?)'''\s*\)", html_content, re.DOTALL)
                
                for tab_id, tab_title, tab_html in tabs_raw:
                    section_soup = BeautifulSoup(tab_html, 'html.parser')
                    section_text = section_soup.get_text(separator="\n", strip=True)
                    chunks = splitter.split_text(section_text)
                    for chunk in chunks:
                        contentList.append([tab_title, chunk, folder, page])

            except Exception as e:
                print(f"⚠️ 탭 파싱 실패 (정규식 버전): {file_path}, {e}")


        else:
            # ✅ 일반 HTML 구조 (<div name="section">) 처리
            soup = BeautifulSoup(html_content, 'html.parser')
            sections = soup.select('[name="section"]')  # 콘텐츠 섹션 추출

            for section in sections:
                titles = section.select('[name="content_title"]')
                title = titles[0].get_text(strip=True) if len(titles) > 0 else ""

                section_text = section.get_text(separator="\n", strip=True)
                chunks = splitter.split_text(section_text)

                for chunk in chunks:
                    contentList.append([title, chunk, folder, page])

    # ✅ 데이터프레임 변환 (확인 및 정제 목적)
    df = pd.DataFrame(contentList, columns=["title", "content", "folder", "page"])

    # ✅ LangChain 문서 객체로 변환 (page_content + 메타데이터)
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
    # embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta")
    # embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    # embedding_model = HuggingFaceEmbeddings(model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS")
    # embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-sts")
    embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta-multitask")

    # ✅ 테스트 출력: '귀어' 키워드가 포함된 chunk 로그 확인
    print("\n📌 '귀어'가 포함된 chunk들:")
    for i, doc in enumerate(documents):
        if "귀어" in doc.page_content:
            print(f"\n[{i}] {doc.metadata.get('source')}")
            print(doc.page_content[:300])

    # ✅ FAISS 벡터 DB 생성 및 저장
    vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
    vectorstore.save_local(out_path)
    print(f"저장 완료: {len(documents)} chunks → {out_path}")

# ✅ 스크립트 직접 실행 시 함수 호출
if __name__ == "__main__":
    extract_and_save_faiss()




# # build_faiss_vectorstore.py
# from bs4 import BeautifulSoup
# from pathlib import Path
# import pandas as pd
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.schema import Document
# import os
# import ast

# def extract_and_save_faiss(base_dir="templates/contents", out_path="faiss_store/contents"):
#     contentList = [] # 문서들의(contents 내의) 모든 chunk를 임시로 모으기

#     # 텍스트 분할
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=600,
#         chunk_overlap=80,
#         separators=["\n\n", "\n", ".", " "],
#     )

#     # templates/contents 하위의 모든 html 파일 탐색
#     for file_path in Path(base_dir).rglob("*.html"):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             html_content = f.read()

#         # 경로에서 폴더명과 파일명을 추출 (메타데이터용)
#         folder = os.path.basename(os.path.dirname(file_path))
#         page = os.path.splitext(os.path.basename(file_path))[0]

#     for file_path in Path(base_dir).rglob("*.html"):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             html_content = f.read()

#         folder = os.path.basename(os.path.dirname(file_path))
#         page = os.path.splitext(os.path.basename(file_path))[0]

#         if '{% set tabs = [' in html_content:
#             tab_start = html_content.index('{% set tabs = [')
#             tab_end = html_content.index('%}', tab_start)
#             tab_block = html_content[tab_start + 16:tab_end]

#             try:
#                 tab_list = ast.literal_eval(tab_block.replace("'", '"'))
#                 for _, _, raw_html in tab_list:
#                     section_soup = BeautifulSoup(raw_html, 'html.parser')
#                     section_text = section_soup.get_text(separator="\n", strip=True)
#                     chunks = splitter.split_text(section_text)
#                     for chunk in chunks:
#                         contentList.append(["스마트양식", chunk, folder, page])
#             except Exception as e:
#                 print(f"⚠️ 탭 파싱 실패: {file_path}, {e}")
#         else:
#             soup = BeautifulSoup(html_content, 'html.parser')
#             sections = soup.select('[name="section"]')
#             for section in sections:
#                 titles = section.select('[name="content_title"]')
#                 title = titles[0].get_text(strip=True) if len(titles) > 0 else ""
#                 section_text = section.get_text(separator="\n", strip=True)
#                 chunks = splitter.split_text(section_text)
#                 for chunk in chunks:
#                     contentList.append([title, chunk, folder, page])

#         # # HTML 파싱
#         # soup = BeautifulSoup(html_content, 'html.parser')

#         # # # div name="section" 태그들 찾기 (conten_title이랑 content_text로 나눠놨음)
#         # sections = soup.select('[name="section"]')
#         # for section in sections:
#         #     titles = section.select('[name="content_title"]')
#         #     # contents = section.select('[name="content_text"]')
#         #     # 제목과 본문이 정확히 하나씩 있을 때만 처리 (1:1로 설정, 정확히 한 쌍일 때만 처리)
#         #     # if len(titles) == 1 and len(contents) == 1:
#         #     #     title = titles[0].get_text(strip=True) # strip으로 태그 제거, 공백 제거
#         #     #     content = contents[0].get_text(strip=True)
#         #     #     # 본문을 chunk 단위로 나누기 -> 정밀도 높이기 위함(너무 길면 정확도 떨어짐..)
#         #     #     chunks = splitter.split_text(content)
#         #     #     for chunk in chunks:
#         #     #         # 각 조각을 리스트에 추가 (title, chunk 내용, 폴더, 파일명)
#         #     #         #contentList.append([title, chunk, folder, page])
#         #     #         contentList.append([title, f"{title}\n{chunk}", folder, page])
            
#         #     # title 먼저 추출 (있을 때만)
#         #     title = titles[0].get_text(strip=True) if len(titles) > 0 else ""

#         #     # 전체 section 텍스트 추출 (title, 본문 등 전부)
#         #     section_text = section.get_text(separator="\n", strip=True)

#         #     # 전체를 합쳐서 의미 기반 벡터 생성에 활용
#         #     # full_text = f"{title}\n{page}\n{section_text}"
#         #     if title and title not in section_text:
#         #         full_text = f"{title}\n{section_text}\n{page}"
#         #     else:
#         #         full_text = f"{section_text}\n{page}"

#         #     chunks = splitter.split_text(full_text)
#         #     for chunk in chunks:
#         #         contentList.append([title, chunk, folder, page])

#     # 데이터프레임으로 변환
#     df = pd.DataFrame(contentList, columns=["title", "content", "folder", "page"])

#     # LangChain Document 객체로 변환 (메타데이터 포함)
#     documents = [
#         Document(
#             page_content=f"{row['title']}\n{row['page']}\n{row['content']}",
#             metadata={
#                 "title": row['title'],
#                 "folder": row['folder'],
#                 "page": row['page'],
#                 "source": f"templates/contents/{row['folder']}/{row['page']}.html"
#             }
#         )
#         for _, row in df.iterrows()
#     ]


#     # 임베딩 모델 LOAD
#     # embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
#     embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta")
#     # embedding_model = HuggingFaceEmbeddings(model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS")
#     # embedding_model = HuggingFaceEmbeddings(model_name="jhgan/ko-sbert-sts")
#     # embedding_model = HuggingFaceEmbeddings(model_name="BM-K/KoSimCSE-roberta-multitask")


#     # 테스트용
#     print("\n📌 '귀어'가 포함된 chunk들:")
#     for i, doc in enumerate(documents):
#         if "귀어" in doc.page_content:
#             print(f"\n[{i}] {doc.metadata.get('source')}")
#             print(doc.page_content[:300])


#     # FAISS 벡터 DB 생성
#     vectorstore = FAISS.from_documents(documents=documents, embedding=embedding_model)
#     vectorstore.save_local(out_path) # 지정 경로에 저장
#     print(f"저장 완료: {len(documents)} chunks → {out_path}") # 완료 로그

# # 스크립트 직접 실행 시 호출
# if __name__ == "__main__":
#     extract_and_save_faiss()
