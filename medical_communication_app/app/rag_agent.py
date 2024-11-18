import os
import json
import yaml
from groq import Groq
from app.database import save_conversation

class RAGAgent:
    def __init__(self, settings_path="config/settings.yaml"):
        with open(settings_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.api_key = config.get("groq", {}).get("api_key", "")
        self.model_name = config.get("llm", {}).get("model_name", "llama3-groq-70b-8192-tool-use-preview")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, conversation_text):
        # 프롬프트 생성
        prompt = self.create_prompt(conversation_text)

        # Groq API를 사용하여 응답 생성
        response_text = self.query_llm(prompt)

        # LLM의 응답을 파싱하여 JSON으로 변환
        try:
            analysis_result = json.loads(response_text)
        except json.JSONDecodeError:
            # JSON 파싱에 실패한 경우 전체 응답을 저장
            analysis_result = {"전체응답": response_text}

        # 대화 및 응답 저장
        save_conversation(conversation_text, analysis_result)

        return analysis_result

    def create_prompt(self, conversation_text):
        # 프롬프트 간소화 및 길이 제한
        max_conversation_length = 1000  # 필요한 경우 조정
        if len(conversation_text) > max_conversation_length:
            conversation_text = conversation_text[:max_conversation_length] + "..."

        prompt = (
            "당신은 의료 소통 전문가입니다. 아래는 의사와 환자의 대화입니다:\n\n"
            f"{conversation_text}\n\n"
            "위 대화를 분석하여 다음 사항에 대해 JSON 형식으로 답변해 주세요:\n"
            "{\n"
            '  "문제점": "",\n'
            '  "개선방안": "",\n'
            '  "개선된대화예시": "",\n'
            '  "점수": "",  # 0부터 100 사이의 숫자로 평가해 주세요.\n'
            '  "평가근거": ""\n'
            "}\n"
            "각 항목의 내용을 적절히 한글로 작성해 주세요."
        )
        return prompt

    def query_llm(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        response = chat_completion.choices[0].message.content.strip()
        return response