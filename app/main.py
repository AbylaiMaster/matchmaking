from fastapi import FastAPI
from app.api import players, queue, matches, leaderboard

app = FastAPI(title="Matchmaking System")

app.include_router(players.router)
app.include_router(queue.router)
app.include_router(matches.router)
app.include_router(leaderboard.router)