class User:
    def __init__(
        self,
        id: int | None,
        username: str,
        email: str,
        password_hash: str,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
