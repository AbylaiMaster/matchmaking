from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.services.matchmaking import find_match
from app.services.elo import calculate_elo
from app.schemas.match import MatchResult
import datetime

router = APIRouter(prefix="/matches", tags=["Matches"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/find")
def matchmake(db: Session = Depends(get_db)):
    match = find_match()

    if not match:
        return {"message": "No match found"}

    p1, p2 = match

    db_match = models.Match(
        player1_id=p1.id,
        player2_id=p2.id,
        created_at=datetime.datetime.utcnow()
    )

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return {
        "match_id": db_match.id,
        "player1": p1.name,
        "player2": p2.name
    }


@router.post("/result")
def set_result(result: MatchResult, db: Session = Depends(get_db)):
    match = db.query(models.Match).get(result.match_id)

    if not match:
        return {"error": "Match not found"}

    if match.status == "finished":
        return {"error": "Match already finished"}

    p1 = db.query(models.Player).get(match.player1_id)
    p2 = db.query(models.Player).get(match.player2_id)

    if result.is_draw:
        p1.rating = calculate_elo(p1.rating, p2.rating, 0.5)
        p2.rating = calculate_elo(p2.rating, p1.rating, 0.5)

        match.status = "finished"

        match.winner_id = None

        db.commit()

        return {
            "message": "Draw recorded",
            "new_ratings": {
                p1.name: p1.rating,
                p2.name: p2.rating
            }
        }

    if result.winner_id == p1.id:
        p1.rating = calculate_elo(p1.rating, p2.rating, 1)
        p2.rating = calculate_elo(p2.rating, p1.rating, 0)
    else:
        p1.rating = calculate_elo(p1.rating, p2.rating, 0)
        p2.rating = calculate_elo(p2.rating, p1.rating, 1)

    match.winner_id = result.winner_id

    match.status = "finished"

    db.commit()

    return {
        "message": "Result recorded",
        "new_ratings": {
            p1.name: p1.rating,
            p2.name: p2.rating
        }
    }