import os
import json 
from app.utils import get_embeddings, search_similar_documents
from app.database import save_conversation
import yaml
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class RAGAgent:
    def __init__(self, settings_path="config/settings.yaml"):
        # 설정 파일 로드
        with open(settings_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        self.knowledge_base_dir = config.get("rag", {}).get("knowledge_base_dir", "data/knowledge_base/")
        self.model_name = config.get("llm", {}).get("model_name", "EleutherAI/polyglot-ko-5.8b")
        self.embeddings, self.documents = get_embeddings(self.knowledge_base_dir)
        # LLM 모델 로드
        self.load_llm_model()

    def load_llm_model(self):
        # LLM 모델 로드
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map='auto',
            torch_dtype=torch.float16
        )
        self.model.eval()

    def generate_response(self, conversation_text):
        # 대화 내용을 임베딩
        query_embedding, _ = get_embeddings([conversation_text])

        # 유사한 문서 검색
        similar_docs = search_similar_documents(query_embedding[0], self.embeddings, self.documents)

        # 프롬프트 생성
        prompt = self.create_prompt(conversation_text, similar_docs)

        # LLM 모델을 사용하여 응답 생성
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

    def create_prompt(self, conversation_text, similar_docs):
        context = "\n".join(similar_docs)
        prompt = (
            f"{context}\n\n"
            "당신은 의료 소통 전문가입니다. 아래는 의사와 환자의 대화입니다:\n\n"
            f"{conversation_text}\n\n"
            "위 대화를 분석하여 다음 사항에 대해 **JSON 형식**으로 답변해 주세요:\n"
            "{\n"
            '  "문제점": "",\n'
            '  "개선방안": "",\n'
            '  "개선된대화예시": "",\n'
            '  "점수": "",  # 0부터 100 사이의 숫자로 평가해 주세요.\n'
            '  "평가근거": ""\n'
            "}\n"
            "각 항목의 내용을 적절히 작성해 주세요."
        )
        return prompt

    def query_llm(self, prompt):
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt').to(self.model.device)
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_length=1024,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                num_beams=5,
                early_stopping=True
            )
        output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # 프롬프트 부분 제거
        response = output[len(prompt):].strip()
        return response