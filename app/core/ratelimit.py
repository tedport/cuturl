from collections import defaultdict, deque

from datetime import datetime, timedelta, timezone

from fastapi import Request

from app.core.exceptions import RateLimitError

ip_request_log: dict[str, deque] = defaultdict(deque)

def check_rate_limit(request: Request):
    ip = request.client.host
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=30)
    log = ip_request_log[ip]
    
    while log and log[0] < window_start:
        log.popleft()
    
    if len(log) >= 10:
        raise RateLimitError()
    
    log.append(now)