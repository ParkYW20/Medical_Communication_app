from app.stt_processor import process_audio_file
from pathlib import Path
import json
from datetime import datetime

def main(audio_file_path):

    transcription_text = process_audio_file(audio_file_path)
    output_path = save_transcription(transcription_text)
    return output_path

def save_transcription(transcription_text):
    
    data = {
        "transcription_text": transcription_text
    }
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"transcription_result_{timestamp}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return output_path