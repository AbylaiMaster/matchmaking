from app.services.queue_manager import queue
import time

def find_match():
    if len(queue) < 2:
        return None

    for i in range(len(queue)):
        for j in range(i + 1, len(queue)):
            p1 = queue[i]
            p2 = queue[j]

            diff = abs(p1["player"].rating - p2["player"].rating)
            wait_time = time.time() - min(p1["joined_at"], p2["joined_at"])

            max_diff = 50 + wait_time * 2

            if diff <= max_diff:
                match = (p1["player"], p2["player"])

                queue.remove(p1)
                queue.remove(p2)

                return match

    return None