from gestor_de_stock.domain.user import User


def test_login_with_incorrect_password(
    client_user, correct_password, api_user_repository, password_hasher
):
    correct_password_hash = password_hasher.hash(correct_password)
    user = User(
        id=None,
        username="adnane",
        email="infadadnan@gmail.com",
        password_hash=correct_password_hash,
    )
    api_user_repository.save(user)

    response = client_user.post(
        "/login", json={"email": "infadadnan@gmail.com", "password": "wrong-password"}
    )

    assert response.status_code == 401


def test_login_with_correct_password(
    client_user, correct_password, api_user_repository, password_hasher
):
    correct_password_hash = password_hasher.hash(correct_password)

    user = User(
        id=None,
        username="adnane",
        email="infadadnan@gmail.com",
        password_hash=correct_password_hash,
    )
    api_user_repository.save(user)
    response = client_user.post(
        "/login", json={"email": "infadadnan@gmail.com", "password": correct_password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_rate_limit(
    client_user, correct_password, api_user_repository, password_hasher
):
    correct_password_hash = password_hasher.hash(correct_password)
    user = User(
        id=None,
        username="adnane",
        email="infadadnan@gmail.com",
        password_hash=correct_password_hash,
    )
    api_user_repository.save(user)
    # 2. Send five requests with an incorrect password
    for _ in range(5):
        response = client_user.post(
            "/login",
            json={"email": "infadadnan@gmail.com", "password": "wrong-password"},
        )
        assert response.status_code == 401
    # 3. Send one more request
    response = client_user.post(
        "/login", json={"email": "infadadnan@gmail.com", "password": "wrong-password"}
    )
    assert response.status_code == 429
