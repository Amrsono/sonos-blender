from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(
    title="Gemini + Blender 3D Motion Graphics API",
    description="API backend for code-driven 3D motion graphics generation.",
    version="1.0.0"
)

class AnimationRequest(BaseModel):
    prompt: str
    duration: int = 5
    fps: int = 30

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Gemini + Blender 3D Motion Graphics Pipeline",
        "message": "Welcome! Use POST /api/generate or run the CLI locally for full Blender + FFmpeg rendering."
    }

@app.post("/api/generate")
def generate_animation(req: AnimationRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable not configured on server.")

    # On Vercel serverless, local Blender & FFmpeg binaries are not present.
    # This endpoint can generate the script or queue the job.
    return {
        "status": "success",
        "message": "Animation prompt received successfully.",
        "prompt": req.prompt,
        "duration": req.duration,
        "fps": req.fps,
        "note": "Full 3D rendering with Blender and FFmpeg runs via CLI or local worker."
    }
