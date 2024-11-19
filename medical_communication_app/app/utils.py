import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_embeddings(knowledge_base_dir):
    documents = []
    for file_name in os.listdir(knowledge_base_dir):
        file_path = os.path.join(knowledge_base_dir, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read().strip())

    documents = [doc for doc in documents if doc]
    if not documents:
        raise ValueError("지식 베이스 디렉터리에 유효한 텍스트 파일이 없습니다.")

    vectorizer = TfidfVectorizer()
    embeddings = vectorizer.fit_transform(documents)
    return embeddings, vectorizer, documents


def get_query_embedding(conversation_text, vectorizer):
    
    query_embedding = vectorizer.transform([conversation_text])
    return query_embedding


def search_similar_documents(query_embedding, embeddings, documents, top_k=3):

    similarity_scores = cosine_similarity(query_embedding, embeddings).flatten()
    top_indices = np.argsort(similarity_scores)[::-1][:top_k]
    similar_docs = [documents[idx] for idx in top_indices]
    return similar_docs