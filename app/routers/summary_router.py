from app.services import download_service
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.post("/summarise")
async def process_audio(url: str, request: Request):
    try:
        download_service = request.app.state.download_service
        llm = request.state.llm
        transcribing_service = request.app.state.transcribing_service
        summarisation_service = request.app.state.summarisation_service

        summary = summarisation_service.summary(
            url=url,
            download_service=download_service,
            llm=llm,
            transcribing_service=transcribing_service,
        )

        return {"status": "success", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
