import os
import uuid
from fastapi import APIRouter, Request, HTTPException, Header, Depends, BackgroundTasks
from pydantic import BaseModel

summary_router = APIRouter()

API_KEY = os.getenv("API_KEY")

# In-memory task store
tasks: dict[str, dict] = {}


class SummariseRequest(BaseModel):
    url: str


async def verify_key(x_api_key: str = Header(...)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


def run_pipeline(task_id: str, url: str, app_state):
    try:
        download_service = app_state.download_service
        llm = app_state.llm
        transcribing_service = app_state.transcribing_service
        summarisation_service = app_state.summarisation_service

        summary = summarisation_service.summary(
            url=url,
            download_service=download_service,
            llm=llm,
            transcribing_service=transcribing_service,
        )
        tasks[task_id] = {"status": "success", "summary": summary}
    except Exception as e:
        tasks[task_id] = {"status": "failed", "detail": str(e)}


@summary_router.post("/summarise")
async def process_audio(
    payload: SummariseRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    _=Depends(verify_key),
):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing"}
    background_tasks.add_task(run_pipeline, task_id, payload.url, request.app.state)
    return {"status": "accepted", "task_id": task_id}


@summary_router.get("/status/{task_id}")
async def get_status(task_id: str, _=Depends(verify_key)):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
