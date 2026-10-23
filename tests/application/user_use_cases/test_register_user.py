import pytest

from gestor_de_stock.application.user_use_cases.register_user import RegisterUser
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_user_repository import FakeUserRepository


def test_register_user():
    fakeUserRepository = FakeUserRepository()
    fakePasswordHasher = FakePasswordHasher(password="adnani1")
    use_case = RegisterUser(fakeUserRepository, fakePasswordHasher)

    user = use_case.execute(
        username="Adnane", email="infadadnan@gmail.com", password="adnani1"
    )
    assert user.username == "Adnane"
    assert user.email == "infadadnan@gmail.com"
    assert user.password_hash == "fake_hashed_password"
    assert fakePasswordHasher.recieved_password == "adnani1"
    assert len(fakeUserRepository.users) == 1


def test_register_existing_user(user):
    fakeUserRepository = FakeUserRepository()
    fakePasswordHasher = FakePasswordHasher(password="adnani1")

    fakeUserRepository.save(user)

    use_case = RegisterUser(fakeUserRepository, fakePasswordHasher)
    with pytest.raises(ValueError):
        use_case.execute(username="Anas", email=user.email, password="adnse")
