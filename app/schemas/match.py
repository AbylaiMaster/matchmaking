from pydantic import BaseModel

class MatchResult(BaseModel):
    match_id: int
    winner_id: int | None = None
    is_draw: bool = False