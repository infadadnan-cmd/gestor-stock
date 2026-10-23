import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from gestor_de_stock.application.ports.rate_limiter import RateLimiter
from gestor_de_stock.infrastructure.security.jwt_service import JWTService
from gestor_de_stock.infrastructure.security.password_hasher import PasswordHasher
from gestor_de_stock.infrastructure.security.rate_limiter import InMemoryRateLimiter

bearer_scheme = HTTPBearer()
load_dotenv()  # Carga las variables de entorno desde el archivo .env


def get_jwt_service():
    secret_key = os.getenv("SECRET_KEY")  # Obtiene la clave secreta desde las variables
    if not secret_key:
        raise RuntimeError("SECRET_KEY is not set in the environment variables.")
    return JWTService(secret_key=secret_key)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    jwt_service=Depends(get_jwt_service),
) -> dict | None:
    token = credentials.credentials
    try:
        verified_token = jwt_service.verify_token(token)
        return verified_token

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


_rate_limiter = InMemoryRateLimiter(window=60, max_attempts=5)


def get_rate_limiter() -> RateLimiter:
    return _rate_limiter


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()
