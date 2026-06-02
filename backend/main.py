"""GraceGuide Python Sidecar — FastAPI server on localhost:3721"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from game_detection.monitor import detect_current_game
from controller.xinput import is_controller_connected, get_controller_state
from onboarding.recommender import recommend, get_build_summary
from chat.router import router as chat_router
from db.user_store import init_db

app = FastAPI(title="GraceGuide Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Health ───────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


# ─── Game Detection ──────────────────────────────────────────────────

@app.get("/game/current")
async def current_game():
    game = detect_current_game()
    return {"game": game, "detected": game is not None}


# ─── Controller ──────────────────────────────────────────────────────

@app.get("/controller/status")
async def controller_status():
    return {
        "connected": is_controller_connected(),
        "state": get_controller_state(),
    }


# ─── Onboarding / Build Recommender ──────────────────────────────────

class RecommendRequest(BaseModel):
    playstyle: str = "unknown"
    difficulty: str = "easy"
    weapon_pref: str | None = None

@app.post("/onboarding/recommend")
async def recommend_build(req: RecommendRequest):
    build = recommend(req.playstyle, req.difficulty, req.weapon_pref)
    summary = get_build_summary(build)
    return {"build": build, "summary": summary}


# ─── Include routers ────────────────────────────────────────────────

app.include_router(chat_router)


# ─── Entry point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    print("Starting GraceGuide backend on http://127.0.0.1:3721")
    uvicorn.run(app, host="127.0.0.1", port=3721, log_level="info")
