import time
from typing import Dict
from fastapi import Request, HTTPException, status


class RateLimiter:
    def __init__(self, times: int, minutes: int):
        self.times = times
        self.minutes = minutes
        self.requests: Dict[str, list] = {}

    def __call__(self, request: Request):
        client_ip = request.client.host
        current_time = time.time()

        # Очищення старих записів
        if client_ip in self.requests:
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < self.minutes * 60]
        else:
            self.requests[client_ip] = []

        self.requests[client_ip].append(current_time)

        if len(self.requests[client_ip]) > self.times:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests. Try again in {self.minutes} minutes."
            )