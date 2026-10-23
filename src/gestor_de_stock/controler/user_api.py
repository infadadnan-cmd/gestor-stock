from fastapi import APIRouter, Depends, HTTPException, Request, status

from gestor_de_stock.application.ports.rate_limiter import RateLimiter
from gestor_de_stock.application.user_use_cases.authenticate_user import (
    AuthenticateUser,
)
from gestor_de_stock.application.user_use_cases.register_user import RegisterUser
from gestor_de_stock.domain.password_hasher import PasswordHasher
from gestor_de_stock.infrastructure.database import connection
from gestor_de_stock.infrastructure.security.dependencies import (
    get_jwt_service,
    get_password_hasher,
    get_rate_limiter,
)
from gestor_de_stock.infrastructure.security.jwt_service import JWTService
from gestor_de_stock.infrastructure.security.password_hasher import PasswordHasher
from gestor_de_stock.infrastructure.sqlite_user_repository import SQLiteUserRepository
from gestor_de_stock.repositories.user_repository import UserRepository
from gestor_de_stock.shemas import LoginResponse, UserLogin, UserRegister, UserResponse

router = APIRouter()
login_attempts = {}
window = 60  # Time window in seconds
max_attempts = 5  # Maximum allowed attempts within the time window


def get_user_repository():
    return SQLiteUserRepository(connection)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(
    user_login: UserLogin,
    request: Request,
    user_repository: UserRepository = Depends(get_user_repository),
    jwt_service: JWTService = Depends(get_jwt_service),
    rate_limiter: RateLimiter = Depends(get_rate_limiter),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    if request.client is None:
        raise HTTPException(status_code=400, detail="Unable to identify the client")
    ip_address = request.client.host
    should_block = rate_limiter.should_block_request(ip_address)
    if should_block:
        raise HTTPException(
            status_code=429, detail="Too many login attempts. Please try again later."
        )

    use_case = AuthenticateUser(user_repository, password_hasher)
    try:
        authenticated_user = use_case.execute(
            email=user_login.email, password=user_login.password
        )
        payload = {
            "user_id": authenticated_user.id,
            "username": authenticated_user.username,
            "email": authenticated_user.email,
        }
        return LoginResponse(
            access_token=jwt_service.generate_token(payload), token_type="bearer"
        )
    except ValueError as e:
        rate_limiter.record_failed_attempt(ip_address)
        raise HTTPException(status_code=401, detail=str(e))


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def register(user: UserRegister, userRepository=Depends(get_user_repository)):
    password_hasher = PasswordHasher()
    use_case = RegisterUser(userRepository, password_hasher)
    try:
        created_user = use_case.execute(
            username=user.username, email=user.email, password=user.password
        )
        return UserResponse.model_validate(created_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
