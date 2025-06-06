import time
from typing import Dict
from collections import defaultdict, deque

MAX_REQUESTS = 10
WINDOW_SIZE = 60

rate_limit_store: Dict[str, deque] = defaultdict(deque)

def is_allowed(ip: str) -> Dict:
    now = time.time()
    window_start = now - WINDOW_SIZE
    q = rate_limit_store[ip]

    while q and q[0] < window_start:
        q.popleft()

    current_count = len(q)
    if current_count >= MAX_REQUESTS:
        return {
            "allowed": False,
            "current_requests": current_count,
            "retry_after": int(q[0] + WINDOW_SIZE - now) if q else 1
        }

    q.append(now)
    return {
        "allowed": True,
        "current_requests": current_count + 1,
        "retry_after": 0
    }

class Limiter:
    def is_allowed(self, ip: str) -> Dict:
        return is_allowed(ip)

limiter = Limiter()
