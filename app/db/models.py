from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.database import Base
import datetime

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Integer, default=1000)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey("players.id"))
    player2_id = Column(Integer, ForeignKey("players.id"))
    winner_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    status = Column(String, default="pending")