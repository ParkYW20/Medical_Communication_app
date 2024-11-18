import whisper
from pyannote.audio import Pipeline
from pyannote.audio.utils.signal import Binarize

def process_audio_file(audio_file_path):

    model = whisper.load_model("base")
    result = model.transcribe(str(audio_file_path), language='ko')

    diarization = perform_speaker_diarization(audio_file_path)

    transcription_text = align_transcription_with_speakers(result['segments'], diarization)

    return transcription_text

def perform_speaker_diarization(audio_file_path):

    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token="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") 
    diarization = pipeline(str(audio_file_path))
    return diarization

def align_transcription_with_speakers(segments, diarization):
 
    speaker_labels = []
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']

        speaker = find_speaker_label(start_time, end_time, diarization)
        speaker_labels.append(f"{speaker}: {text.strip()}")
    transcription_text = "\n".join(speaker_labels)
    return transcription_text

def find_speaker_label(start_time, end_time, diarization):
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.start <= start_time and turn.end >= end_time:
            return speaker
    return "Unknown"