import os
from app.services import download_service
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from pydantic import BaseModel

summary_router = APIRouter()


class SummariseRequest(BaseModel):
    url: str


API_KEY = os.getenv("API_KEY")


async def verify_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@summary_router.post("/summarise")
async def process_audio(
    payload: SummariseRequest, request: Request, _=Depends(verify_key)
):
    try:
        download_service = request.app.state.download_service
        llm = request.app.state.llm
        transcribing_service = request.app.state.transcribing_service
        summarisation_service = request.app.state.summarisation_service

        summary = summarisation_service.summary(
            url=payload.url,
            download_service=download_service,
            llm=llm,
            transcribing_service=transcribing_service,
        )

        return {"status": "success", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
