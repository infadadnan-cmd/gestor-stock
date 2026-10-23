from abc import ABC, abstractmethod

from gestor_de_stock.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, user_email: str) -> User | None:
        pass
