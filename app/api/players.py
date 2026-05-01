from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db import models
from app.schemas.player import PlayerCreate, PlayerOut, PlayerUpdate
from app.services.queue_manager import leave_queue

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/players", tags=["Players"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlayerOut)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = models.Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@router.get("/", response_model=list[PlayerOut])
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()

@router.put("/{player_id}", response_model=PlayerOut)
def update_player(player_id: int, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.query(models.Player).get(player_id)

    if not player:
        return {"error": "Player not found"}

    if player_data.name is not None:
        player.name = player_data.name

    if player_data.rating is not None:
        player.rating = player_data.rating

    db.commit()
    db.refresh(player)

    return player

@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).get(player_id)

    if not player:
        return {"error": "Player not found"}
    
    leave_queue(player_id)

    db.delete(player)
    db.commit()

    return {"message": "Player deleted"}

@router.get("/{player_id}/matches")
def get_player_matches(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).get(player_id)

    if not player:
        return {"error": "Player not found"}

    matches = db.query(models.Match).filter(
        (models.Match.player1_id == player_id) |
        (models.Match.player2_id == player_id)
    ).all()

    result = []

    for m in matches:
        opponent_id = m.player2_id if m.player1_id == player_id else m.player1_id
        opponent = db.query(models.Player).get(opponent_id)

        if m.status == "pending":
            result_str = "pending"
        elif m.winner_id is None:
            result_str = "draw"
        elif m.winner_id == player_id:
            result_str = "win"
        else:
            result_str = "lose"

        result.append({
            "match_id": m.id,
            "opponent": opponent.name if opponent else "Unknown",
            "winner_id": m.winner_id,
            "result": result_str,
            "played_at": m.created_at
        })

    return result