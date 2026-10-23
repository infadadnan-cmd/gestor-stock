from gestor_de_stock.domain.user import User
from gestor_de_stock.infrastructure.security.password_hasher import PasswordHasher
from gestor_de_stock.repositories.user_repository import UserRepository


class RegisterUser:
    def __init__(
        self,
        userRepository: UserRepository,
        passwordHasher: PasswordHasher,
    ):
        self.userRepository = userRepository
        self.passwordHasher = passwordHasher

    def execute(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:
        existing_user = self.userRepository.get_by_email(email)
        if existing_user is not None:
            raise ValueError("Email already registred")
        password_hash = self.passwordHasher.hash(password)
        user = User(
            id=None, username=username, email=email, password_hash=password_hash
        )
        self.userRepository.save(user)
        return user
