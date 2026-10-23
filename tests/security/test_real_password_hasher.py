def test_hash_password(password_hasher):
    password = "Adnani1"
    password_hash = password_hasher.hash(password)
    assert password_hash != password


def test_verify_correct_password(password_hasher):
    password = "Adnani1"
    password_hash = password_hasher.hash(password)
    result = password_hasher.verify(password, password_hash)
    assert result is True


def test_verify_incorrect_password(password_hasher):
    password = "Adnani1"
    password_hash = password_hasher.hash(password)
    result = password_hasher.verify("incorrect password", password_hash)
    assert result is False
