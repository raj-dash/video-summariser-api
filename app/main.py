from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.download_service import DownloadService
from app.services.llm_service import LlmService
from app.services.transcribing_service import TranscribingService
from app.services.summarisation_service import SummarisationService

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.download_service = DownloadService()
    app.state.llm = LlmService()
    app.state.transcribing_service = TranscribingService()
    app.summarisation_service = SummarisationService()

    yield


app = FastAPI(
    title="Audio Summarization & Transcription API",
    description="A backend service for downloading, transcribing, and processing audio files with Gemini.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/", tags=["Health Check"])
    async def root_health_check():
        """Basic health check endpoint at the base URL."""
        return {
            "status": "healthy",
            "service": "audio-summarization-api",
            "environment": os.getenv("ENV", "development")
        }

    return app
