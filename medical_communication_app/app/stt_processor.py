import whisper

class STTProcessor:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self, audio_path):
        result = self.model.transcribe(audio_path)
        return result['text'], result['segments']