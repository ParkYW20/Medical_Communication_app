import yaml
import json
from app.stt_processor import STTProcessor
from app.diarization_processor import DiarizationProcessor
from app.llm_analyzer import LLMAnalyzer

def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def merge_stt_diarization(transcription_segments, speaker_segments):
    merged_results = []
    for seg in transcription_segments:
        start, end = seg['start'], seg['end']
        speaker = next(
            (spk['speaker'] for spk in speaker_segments if spk['start'] <= start < spk['end']),
            "Unknown"
        )
        merged_results.append({"start": start, "end": end, "speaker": speaker, "text": seg['text']})
    return merged_results

def main():
    config = load_config("config/settings.yaml")

    stt_processor = STTProcessor(model_size="base")
    diarization_processor = DiarizationProcessor(
        auth_token=config["pyannote"]["auth_token"],
        model_name=config["pyannote"]["model_name"]
    )
    llm_analyzer = LLMAnalyzer(model_name=config["llm"]["model_name"])

    audio_path = config["audio"]["input_path"]
    text, transcription_segments = stt_processor.transcribe_audio(audio_path)
    speaker_segments = diarization_processor.diarize_audio(audio_path)
    merged_results = merge_stt_diarization(transcription_segments, speaker_segments)

    analysis_results = llm_analyzer.analyze_conversation(text)

    output_path = config["audio"]["output_path"]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"merged_results": merged_results, "analysis": analysis_results}, f, ensure_ascii=False, indent=4)

    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()