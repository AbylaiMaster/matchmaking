# Matchmaking System (Backend)

## Description
This project is a backend matchmaking system designed to pair players and manage game matches. It provides functionality for player management, queue-based matchmaking, and rating calculation based on match results.

---

## Features
- Player management (create, update, delete)
- Queue system for matchmaking
- Matchmaking algorithm
- ELO rating system
- Support for match results: win, loss, draw
- Match history tracking
- Match status management (pending / finished)
- Data validation and error handling

## Getting Started

### 1. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy
```

### 2. Run the server
```bash
uvicorn app.main:app --reload
```

### 3. API documentation
After running:
```
http://127.0.0.1:8000/docs
```

---

## API Examples

### Create player
```
POST /players
```

### Get all players
```
GET /players
```

### Find match
```
POST /matches/find
```

### Submit result
```
POST /matches/result
```

Example (draw):
```json
{
  "match_id": 1,
  "is_draw": true
}
```

---

## System Logic

### Matchmaking
Players join a queue and are automatically paired based on their rating.

### Rating System (ELO)
After each match, player ratings are updated:
- Win → rating increases  
- Loss → rating decreases  
- Draw → both players are adjusted  

---

## Validation
- Prevents duplicate queue entries  
- Prevents submitting match results multiple times  
- Validates player and match existence  

---

## Technologies Used
- Python  
- FastAPI  
- SQLAlchemy  
- SQLite  

---

## Future Improvements
- Use a production-ready database (e.g., PostgreSQL)  
- Add authentication system  
- Develop a frontend interface  
- Improve matchmaking algorithm  

---
