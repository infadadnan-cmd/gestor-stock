from abc import ABC, abstractmethod


class RateLimiter(ABC):
    @abstractmethod
    def should_block_request(self, client_id: str) -> bool:
        pass

    @abstractmethod
    def record_failed_attempt(self, client_id: str) -> None:
        pass
