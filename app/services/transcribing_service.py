from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)


class TranscribingService:
    def __init__(self):
        self.model = WhisperModel("base", device="cpu", compute_type="float32")

    def transcribe(self, file: str):
        segments, info = self.model.transcribe(file, beam_size=5)

        transcript = ""
        for segment in segments:
            transcript += segment.text.strip() + " "

        transcript = transcript.strip()

        return transcript


if __name__ == "__main__":
    obj = TranscribingService()
    file = "app/downloads/Even The Steam Deck Got Hit.mp3"
    transcript = obj.transcribe(file)
    logger.info(transcript)
