from gestor_de_stock.domain.user import User
from gestor_de_stock.repositories.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    def __init__(self):
        self.requested_id = None
        self.users = []

    def save(self, user: User) -> None:
        user.id = 1
        self.users.append(user)

    def get_by_email(self, user_email=str) -> User | None:
        for user in self.users:
            if user.email == user_email:
                return user
        return None
