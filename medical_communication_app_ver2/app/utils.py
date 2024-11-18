import os
import numpy as np
from sentence_transformers import SentenceTransformer

def get_embeddings(texts_or_dir):
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    if isinstance(texts_or_dir, list):
        documents = texts_or_dir
    else:
        documents = []
        for filename in os.listdir(texts_or_dir):
            file_path = os.path.join(texts_or_dir, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents.append(f.read())
    embeddings = model.encode(documents)
    return embeddings, documents

def search_similar_documents(query_embedding, embeddings, documents, top_k=5):
    # 코사인 유사도를 사용하여 유사한 문서 검색
    embeddings = np.array(embeddings)
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    top_indices = similarities.argsort()[-top_k:][::-1]
    similar_docs = [documents[i] for i in top_indices]
    return similar_docs