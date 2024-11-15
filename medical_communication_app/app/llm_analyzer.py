from transformers import pipeline

class LLMAnalyzer:
    def __init__(self, model_name="EleutherAI/gpt-neo-125M"):
        self.nlp_pipeline = pipeline("text-generation", model=model_name)

    def analyze_conversation(self, conversation_text):
        result = self.nlp_pipeline(
            conversation_text,
            max_new_tokens=500,  
            num_return_sequences=1,
            truncation=True
        )
        return result[0]["generated_text"]