from datetime import datetime, timedelta, timezone

import jwt
import pytest


def test_generate_token(jwt_service):
    payload = {"user_id": 1, "username": "testuser"}
    token = jwt_service.generate_token(payload)
    assert token is not None
    assert isinstance(token, str)


def test_verify_token(jwt_service):
    payload = {"user_id": 1, "username": "testuser"}
    token = jwt_service.generate_token(payload)
    verified_payload = jwt_service.verify_token(token)
    assert verified_payload["user_id"] == payload["user_id"]
    assert verified_payload["username"] == payload["username"]
    assert "exp" in verified_payload  # Ensure the expiration time is present


def test_invalid_token(jwt_service):
    invalid_token = "invalid.token.string"
    with pytest.raises(ValueError) as error:
        jwt_service.verify_token(invalid_token)
        assert str(error.value) == "Invalid token"


def test_expired_token(jwt_service):
    payload = {"user_id": 1, "username": "testuser"}
    expiration = datetime.now(timezone.utc) - timedelta(seconds=10)
    payload["exp"] = expiration
    token = jwt.encode(payload, jwt_service.secret_key, algorithm="HS256")

    with pytest.raises(ValueError) as error:
        jwt_service.verify_token(token)
        assert str(error.value) == "Token has expired"
