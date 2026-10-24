from gestor_de_stock.domain.password_hasher import PasswordHasher


class FakePasswordHasher(PasswordHasher):
    def __init__(self, password: str):
        self.recieved_password = password
        self.fake_hash = "fake_hashed_password"

    def hash(self, password: str) -> str:
        self.recieved_password = password
        return self.fake_hash

    def verify(self, password: str, password_hash: str) -> bool:
        return (
            password == self.recieved_password
            and password_hash == "fake_hashed_password"
        )
