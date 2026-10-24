import time

from gestor_de_stock.application.ports.rate_limiter import RateLimiter


class InMemoryRateLimiter(RateLimiter):
    def __init__(self, window: float, max_attempts: int):
        self.login_attempts = {}
        self.window = window
        self.max_attempts = max_attempts

    def should_block_request(self, client_id: str) -> bool:
        current_time = time.monotonic()
        client_attempts = self.login_attempts.get(client_id, [])
        self._cleanup_old_attempts(client_attempts, current_time)
        return self._is_rate_limited(client_attempts, current_time)

    def record_failed_attempt(self, client_id: str) -> None:
        current_time = time.monotonic()
        if client_id not in self.login_attempts:
            self.login_attempts[client_id] = []
        self.login_attempts[client_id].append(current_time)

    def _cleanup_old_attempts(self, attempts: list[float], current_time: float) -> None:
        attempts[:] = [
            attempt
            for attempt in attempts
            if 0 <= current_time - attempt <= self.window
        ]

    def _get_recent_attempts(
        self, attempts: list[float], current_time: float
    ) -> list[float]:
        recent_attempts = []
        for attempt in attempts:
            if 0 <= current_time - attempt <= self.window:
                recent_attempts.append(attempt)
        return recent_attempts

    def _is_rate_limited(self, attempts: list[float], current_time: float) -> bool:
        recent_attempts = self._get_recent_attempts(attempts, current_time)
        return len(recent_attempts) >= self.max_attempts
