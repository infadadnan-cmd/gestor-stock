from gestor_de_stock.infrastructure.security.password_hasher import PasswordHasher


def test_hash_password() -> str:
    hasher = PasswordHasher()

    password = "adnan1"
    password_hash = hasher.hash(password)

    assert password_hash != password


def test_verify_correct_password() -> bool:
    hasher = PasswordHasher()

    correct_password = "adnan1"
    password_hash = hasher.hash(correct_password)

    result = hasher.verify(correct_password, password_hash)

    assert result is True


def test_verify_incorrect_password() -> bool:
    hasher = PasswordHasher()

    correct_password = "adnan1"
    wrong_password = "dxdiag"

    password_hash = hasher.hash(correct_password)

    result = hasher.verify(wrong_password, password_hash)

    assert result is False
