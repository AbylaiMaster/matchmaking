from pydantic import BaseModel

class PlayerCreate(BaseModel):
    name: str

class PlayerOut(BaseModel):
    id: int
    name: str
    rating: int

    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    name: str | None = None
    rating: int | None = None