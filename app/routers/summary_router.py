from fastapi import APIRouter, Request, HTTPException

router = APIRouter()


@router.post("/summarise")
async def process_audio(url: str, request: Request):
    pass
