from pyannote.audio import Pipeline

class DiarizationProcessor:
    def __init__(self, auth_token, model_name):
        self.pipeline = Pipeline.from_pretrained(model_name, use_auth_token=auth_token)

    def diarize_audio(self, audio_path):
        diarization = self.pipeline(audio_path)
        speaker_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
        return speaker_segments