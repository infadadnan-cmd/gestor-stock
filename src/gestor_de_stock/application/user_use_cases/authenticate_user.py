from gestor_de_stock.domain.password_hasher import PasswordHasher
from gestor_de_stock.repositories.user_repository import UserRepository


class AuthenticateUser:
    def __init__(self, userRepository: UserRepository, passwordHasher: PasswordHasher):
        self.userRepository = userRepository
        self.passwordHasher = passwordHasher

    def execute(self, email: str, password: str):
        existing_user = self.userRepository.get_by_email(email)
        if existing_user is None:
            raise ValueError("Email not registred")
        password_correct = self.passwordHasher.verify(
            password, existing_user.password_hash
        )
        if password_correct is True:
            return existing_user
        raise ValueError("incorrect password")
