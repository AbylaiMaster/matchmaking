from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    players = db.query(models.Player).order_by(models.Player.rating.desc()).all()

    return [
        {"name": p.name, "rating": p.rating}
        for p in players
    ]