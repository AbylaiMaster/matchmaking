import time

queue = []

def join_queue(player):
    if any(q["player"].id == player.id for q in queue):
        return False

    queue.append({
        "player": player,
        "joined_at": time.time()
    })

    return True

def leave_queue(player_id):
    global queue
    queue = [q for q in queue if q["player"].id != player_id]

def get_queue():
    return queue