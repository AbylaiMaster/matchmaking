from app.services.queue_manager import queue
from app.db import models

def find_match(db):
    if len(queue) < 2:
        return None

    q1 = queue.pop(0)
    q2 = queue.pop(0)

    p1 = db.query(models.Player).get(q1["player_id"])
    p2 = db.query(models.Player).get(q2["player_id"])

    return p1, p2