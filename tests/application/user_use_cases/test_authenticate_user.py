import pytest

from gestor_de_stock.application.user_use_cases.authenticate_user import (
    AuthenticateUser,
)
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_user_repository import FakeUserRepository


def test_authenticate_existing_user(user):
    fakeUserRepository = FakeUserRepository()
    fakePasswordHasher = FakePasswordHasher(password="adnani1")

    fakeUserRepository.save(user)
    use_case = AuthenticateUser(fakeUserRepository, fakePasswordHasher)

    existing_user = use_case.execute(email=user.email, password="adnani1")
    assert existing_user.email == "infadadnan@gmail.com"
    assert existing_user.password_hash == "fake_hashed_password"
    assert fakePasswordHasher.recieved_password == "adnani1"
    assert existing_user == user


def test_authenticate_user_with_incorrect_password(user):
    fakeUserRepository = FakeUserRepository()
    password_hasher = FakePasswordHasher(password="adnani1")

    fakeUserRepository.save(user)
    use_case = AuthenticateUser(fakeUserRepository, password_hasher)
    with pytest.raises(ValueError):
        use_case.execute(email=user.email, password="dxdiag")


def test_authenticate_user_with_unregistered_email(user):
    fakeUserRepository = FakeUserRepository()
    fakePasswordHasher = FakePasswordHasher(password="adnani1")

    fakeUserRepository.save(user)
    use_case = AuthenticateUser(fakeUserRepository, fakePasswordHasher)
    with pytest.raises(ValueError):
        use_case.execute(email="unregistred email", password="dxdiag")
