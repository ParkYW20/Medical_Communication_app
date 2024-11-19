import os
import json
import torch
import yaml
from datetime import datetime
from pathlib import Path
import whisper
from pyannote.audio import Pipeline
from groq import Groq


class STTProcessor:
    def __init__(self, settings_path="config/settings.yaml"):
        with open(settings_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = whisper.load_model("turbo", device=self.device)

        # Groq 설정
        self.api_key = config.get("groq", {}).get("api_key", "")
        self.client = Groq(api_key=self.api_key)
        self.llm_model_name = config.get("llm", {}).get("model_name", "llama3-groq-70b-8192-tool-use-preview")

        # Hugging Face pyannote.audio Pipeline 설정
        hf_token = config.get("huggingface", {}).get("access_token", "")
        if not hf_token:
            raise ValueError("Hugging Face API 토큰이 설정되지 않았습니다.")
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

    def preprocess_text(self, text):
        """
        STT 결과를 전처리하여 불필요한 유니코드 문자나 특수문자를 제거합니다.
        """
        # 불필요한 유니코드 문자와 특수문자 제거
        cleaned_text = ''.join(c for c in text if c.isprintable())
        return cleaned_text.strip()

    def process_audio(self, audio_path):
        # 화자 분리 수행
        diarization_result = self.diarization_pipeline(audio_path, num_speakers=2)

        # 오디오 파일 로드
        audio = whisper.load_audio(audio_path)
        sample_rate = whisper.audio.SAMPLE_RATE

        # 화자별로 음성 추출 및 STT 수행
        segments = []
        for segment in diarization_result.itertracks(yield_label=True):
            start_time = segment[0].start
            end_time = segment[0].end
            speaker = segment[2]

            # 해당 구간의 오디오 추출
            start_sample = int(start_time * sample_rate)
            end_sample = int(end_time * sample_rate)
            audio_segment = audio[start_sample:end_sample]

            # STT 수행
            result = self.model.transcribe(audio_segment, language='ko')
            transcription_text = result['text']

            # 전처리 수행
            preprocessed_text = self.preprocess_text(transcription_text)

            # LLM을 통한 텍스트 교정
            corrected_text = self.correct_text_with_llm(preprocessed_text)

            segments.append({
                "speaker": speaker,
                "start": start_time,
                "end": end_time,
                "text": corrected_text
            })

        # 결과를 JSON 파일로 저장
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = {"segments": segments}
        os.makedirs("output", exist_ok=True)
        output_path = Path("output") / f"{Path(audio_path).stem}_{timestamp}_transcription.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)

        return output_path

    def correct_text_with_llm(self, text):
        # 프롬프트 생성
        prompt = f"다음 텍스트는 의료진과 환자의 소통 대화입니다. 한글 문법과 표현 및 맞춤법에 맞게 교정해 주세요:\n\n{text}"

        try:
            # Groq API를 사용하여 LLM 호출
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.llm_model_name,
            )
            corrected_text = chat_completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API 오류 발생: {e}")
            corrected_text = text  # 오류 발생 시 원본 텍스트 반환

        return corrected_text