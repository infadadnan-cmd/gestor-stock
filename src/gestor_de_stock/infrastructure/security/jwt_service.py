from datetime import datetime, timedelta, timezone

import jwt


class JWTService:
    def __init__(
        self, secret_key: str = "your_secret_key", expiration_time: int = 1800
    ):
        self.secret_key = secret_key
        self.expiration_time = expiration_time

    def generate_token(self, payload: dict) -> str:
        payload = payload.copy()
        expiration = datetime.now(timezone.utc) + timedelta(
            seconds=self.expiration_time
        )
        payload["exp"] = expiration

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def verify_token(self, token: str) -> dict | None:
        # Logic to verify the JWT token and return the payload if valid
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
