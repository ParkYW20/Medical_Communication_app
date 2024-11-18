from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "EleutherAI/polyglot-ko-1.3b"  # 더 작은 모델로 변경

# 토크나이저 다운로드 및 저장
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained("models/polyglot-ko-1.3b")

# 모델 다운로드 및 저장
model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained("models/polyglot-ko-1.3b")

print("모델과 토크나이저가 다운로드되어 'models/polyglot-ko-1.3b' 디렉터리에 저장되었습니다.")