from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.services.queue_manager import join_queue, get_queue

router = APIRouter(prefix="/queue", tags=["Queue"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/join/{player_id}")
def join(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).get(player_id)
    if not player:
        return {"error": "Player not found"}

    success = join_queue(player)

    if not success:
        return {"error": "Player already in queue"}

    return {"message": "Joined queue"}

@router.get("/")
def show_queue():
    return [{"player_id": q["player"].id} for q in get_queue()]