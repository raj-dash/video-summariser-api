from app.services.download_service import DownloadService
from app.services.llm_service import LlmService
from app.services.transcribing_service import TranscribingService


class SummarisationService:
    def __init__(self):
        pass

    def summary(
        self,
        url: str,
        download_service: DownloadService,
        llm: LlmService,
        transcribing_service: TranscribingService,
    ):
        download_service.download_video(url=url)
