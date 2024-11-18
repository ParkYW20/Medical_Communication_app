import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_embeddings(knowledge_base_dir):
    # 디렉터리에서 텍스트 파일 읽기
    documents = []
    for file_name in os.listdir(knowledge_base_dir):
        file_path = os.path.join(knowledge_base_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read().strip())

    # 빈 문서 필터링
    documents = [doc for doc in documents if doc]
    if not documents:
        raise ValueError("지식 베이스 디렉터리에 유효한 텍스트 파일이 없습니다.")

    # TF-IDF 벡터라이저 생성 및 학습
    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(documents)
    return embeddings, vectorizer, documents

def get_query_embedding(conversation_text, vectorizer):
    # 기존의 벡터라이저를 사용하여 쿼리 임베딩 생성
    query_embedding = vectorizer.transform([conversation_text])
    return query_embedding

def search_similar_documents(query_embedding, embeddings, documents, top_k=3):
    # 코사인 유사도 계산
    similarity_scores = cosine_similarity(query_embedding, embeddings).flatten()
    # 유사도 점수 기준으로 정렬
    top_indices = np.argsort(similarity_scores)[::-1][:top_k]
    # 가장 유사한 문서 반환
    similar_docs = [documents[idx] for idx in top_indices]
    return similar_docs