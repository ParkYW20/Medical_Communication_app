import os
import json
import yaml
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from app.utils import get_embeddings, get_query_embedding, search_similar_documents
from app.database import save_conversation


class RAGAgent:
    def __init__(self, settings_path="config/settings.yaml"):
        with open(settings_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.api_key = config.get("groq", {}).get("api_key", "")
        self.model_name = config.get("llm", {}).get("model_name", "llama3-groq-70b-8192-tool-use-preview")
        self.client = Groq(api_key=self.api_key)

        # Knowledge Base 설정
        knowledge_base_dir = config.get("knowledge_base", {}).get("directory", "data/knowledge_base")
        self.embeddings, self.vectorizer, self.documents = get_embeddings(knowledge_base_dir)

    def generate_response(self, conversation_text):
        # 가장 유사한 문서 검색
        query_embedding = get_query_embedding(conversation_text, self.vectorizer)
        similar_docs = search_similar_documents(query_embedding, self.embeddings, self.documents, top_k=3)

        # 문서들을 프롬프트에 추가
        knowledge_context = "\n\n".join(similar_docs)

        # LLM 호출
        prompt = self.create_prompt(conversation_text, knowledge_context)
        response_text = self.query_llm(prompt)

        # 결과 저장 및 반환
        try:
            analysis_result = json.loads(response_text)
        except json.JSONDecodeError:
            analysis_result = {"전체응답": response_text}

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_conversation(
            conversation_text=conversation_text,
            analysis_result=analysis_result,
            timestamp=timestamp
        )

        return analysis_result

    def create_prompt(self, conversation_text, knowledge_context):
        # 프롬프트 생성 (8000 토큰 한계 고려)
        max_conversation_length = 1000
        if len(conversation_text) > max_conversation_length:
            conversation_text = conversation_text[:max_conversation_length] + "..."

        prompt = (
            "당신은 의료 소통 전문가이며, 의사와 환자의 대화에서 의사의 소통 기술을 분석하고 개선 방안을 제시하는 역할을 맡고 있습니다.\n\n"
            "아래는 의사와 환자의 대화입니다:\n\n"
            f"{conversation_text}\n\n"
            "다음은 대화 분석을 위한 관련된 지식 정보입니다:\n\n"
            f"{knowledge_context}\n\n"
            "위 내용을 바탕으로 의사의 소통 기술을 평가하고, 아래 형식에 맞게 JSON 리포트를 작성해 주세요. "
            "리포트는 명확하고 전문적인 어조로 작성하며, 각 항목에 대한 근거를 구체적으로 포함해야 합니다:\n\n"
            "{\n"
            '  "대화의 문제점": "<의사 소통에서 나타난 주요 문제점과 그 이유를 구체적으로 설명>",\n'
            '  "개선 방안": "<문제점을 해결하기 위한 실행 가능한 개선 방안>",\n'
            '  "개선된 대화 예시": "<위 개선 방안을 적용했을 때의 대화 예문>",\n'
            '  "소통 점수": "<0부터 100 사이의 점수>",\n'
            '  "평가 근거": "<점수의 이유와 분석된 대화 및 관련 지식 정보에 기반한 구체적인 설명>"\n'
            "}\n\n"
            "리포트를 한글로 작성하며, 가능한 명확하고 구체적인 정보를 근거와 함께 제공해 주세요."
        )
        return prompt

    def query_llm(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
        )
        response = chat_completion.choices[0].message.content.strip()
        return response