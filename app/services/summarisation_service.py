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
        path = download_service.download_video(url=url)
        transcript = transcribing_service.transcribe(file=path)
        summary = llm.llm_response(query=transcript)

        return summary


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    llm = LlmService()
    t = TranscribingService()
    d = DownloadService()
    s = SummarisationService()
    summary = s.summary(
        url="https://www.youtube.com/watch?v=g291trLaqTA",
        download_service=d,
        llm=llm,
        transcribing_service=t,
    )
    print(summary)
