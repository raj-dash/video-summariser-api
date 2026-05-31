# Video Summariser API

A FastAPI backend that downloads, transcribes, and summarises video content using AI. Accepts a video URL and returns a markdown summary.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- **Async task pipeline** — jobs are processed in the background, returning a `task_id` instantly to avoid gateway timeouts (Cloudflare 524)
- **Video download** — fetches audio from YouTube, Vimeo, and direct video links via `yt-dlp`
- **Transcription** — converts audio to text using `faster-whisper`
- **AI summarisation** — generates structured markdown summaries via Google Gemini (`google-genai`)
- **API key authentication** — all endpoints gated behind an `x-api-key` header
- **CORS support** — configured for cross-origin frontend access

## Architecture

```
Client                    API                         Background Worker
  │                        │                                │
  ├── POST /summarise ────►│── spawn task ─────────────────►│
  │◄── { task_id } ────────│                                │
  │                        │                    download ──►│
  │                        │                  transcribe ──►│
  │                        │                   summarise ──►│
  │                        │                                │
  ├── GET /status/{id} ───►│◄── { status: "processing" }    │
  ├── GET /status/{id} ───►│◄── { status: "processing" }    │
  ├── GET /status/{id} ───►│◄── { status: "success", summary: "..." }
  │                        │                                │
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)
- A Google Gemini API key

## Getting Started

### 1. Clone and configure

```bash
cd backend-app
cp .env.example .env
```

Edit `.env` with your credentials:

```env
API_KEY=your-api-key-for-endpoint-auth
GEMINI_API_KEY=your-google-gemini-api-key
```

### 2. Build and run

```bash
docker compose up --build -d
```

The API will be available at `http://localhost:7500`.

### 3. Verify

```bash
curl http://localhost:7500/
```

Expected response:

```json
{
  "status": "healthy",
  "service": "audio-summarization-api"
}
```

## API Reference

All endpoints require the `x-api-key` header.

### Health Check

```
GET /
```

Returns service health status. No authentication required.

### Submit a summarisation job

```
POST /summarise
Content-Type: application/json
x-api-key: your-api-key

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response** (immediate):

```json
{
  "status": "accepted",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Poll task status

```
GET /status/{task_id}
x-api-key: your-api-key
```

**Response** (processing):

```json
{
  "status": "processing"
}
```

**Response** (complete):

```json
{
  "status": "success",
  "summary": "## Video Summary\n\nKey points from the video..."
}
```

**Response** (failed):

```json
{
  "status": "failed",
  "detail": "Error description"
}
```

## Docker Compose

```yaml
services:
  video-summariser:
    image: video-summariser
    container_name: video-summariser-api
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "7500:7500"
    env_file:
      - .env
    volumes:
      - downloads:/app/downloads
      - hf_model_cache:/root/.cache/huggingface
    environment:
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

volumes:
  downloads:
    driver: local
  hf_model_cache:
```

The `hf_model_cache` volume persists Hugging Face / Whisper model files across container restarts so they don't re-download each time.

## Deployment with Cloudflare Tunnel

The API is designed to run behind a Cloudflare Tunnel to avoid exposing ports directly.

1. Set up a [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) pointing to `http://localhost:7500`
2. In the Zero Trust dashboard, enable **"Allow OPTIONS Bypass"** for the application to let CORS preflight requests through
3. Optionally add a Cloudflare Access policy to restrict who can reach the tunnel
   The async polling architecture ensures no single request exceeds Cloudflare's 100-second connection timeout.

## Tech Stack

| Component      | Technology                     |
| -------------- | ------------------------------ |
| Framework      | FastAPI (async, lifespan init) |
| Server         | Uvicorn + uvloop               |
| Video Download | yt-dlp + ffmpeg                |
| Transcription  | faster-whisper                 |
| Summarisation  | Google Gemini (google-genai)   |
| Validation     | Pydantic v2                    |
| Runtime        | Python 3.13.5-slim (Docker)    |

## Project Structure

```
backend-app/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── app/
    ├── main.py                 # FastAPI app, lifespan, middleware, health check
    ├── routes/
    │   └── summary.py          # /summarise and /status endpoints
    └── services/
        ├── download_service.py     # yt-dlp video/audio download
        ├── transcribing_service.py # faster-whisper transcription
        └── summarisation_service.py # Gemini summarisation
```

## Environment Variables

| Variable         | Required | Description                         |
| ---------------- | -------- | ----------------------------------- |
| `API_KEY`        | Yes      | Key for authenticating API requests |
| `GEMINI_API_KEY` | Yes      | Google Gemini API key               |

## Notes

- Task state is stored **in-memory** — it resets on container restart. For persistence, swap the `tasks` dict for Redis.
- The `downloads` volume stores temporary audio files during processing.
- CORS middleware must be registered **before** any other middleware in `main.py`.

## License

MIT
