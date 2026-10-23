from tests.fakes.fake_password_hasher import FakePasswordHasher


def test_password_hasher():
    fakePasswordHasher = FakePasswordHasher(password="Adnani1")
    password = "Adnani1"
    password_hash = fakePasswordHasher.hash(password)
    assert password_hash != password


def test_verify_correct_password():
    fakePasswordHasher = FakePasswordHasher(password="Adnani1")
    password = "Adnani1"
    password_hash = fakePasswordHasher.hash(password)
    result = fakePasswordHasher.verify(password, password_hash)
    assert result is True


def test_verify_incorrect_password():
    fakePasswordHasher = FakePasswordHasher(password="Adnani1")
    password_hash = fakePasswordHasher.hash("adnani1")
    result = fakePasswordHasher.verify("incorrect password", password_hash)
    assert result is False
