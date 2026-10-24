import sqlite3

import pytest
from fastapi.testclient import TestClient

from gestor_de_stock.controler.category_api import get_category_repository
from gestor_de_stock.controler.product_api import app, get_product_repository
from gestor_de_stock.controler.user_api import get_user_repository
from gestor_de_stock.domain.category import Category
from gestor_de_stock.domain.product import Product
from gestor_de_stock.domain.user import User
from gestor_de_stock.infrastructure.security.dependencies import (
    get_current_user,
    get_rate_limiter,
)
from gestor_de_stock.infrastructure.security.jwt_service import JWTService
from gestor_de_stock.infrastructure.security.password_hasher import PasswordHasher
from gestor_de_stock.infrastructure.security.rate_limiter import InMemoryRateLimiter
from gestor_de_stock.infrastructure.sqlite_category_repository import (
    SQLiteCategoryRepository,
)
from gestor_de_stock.infrastructure.sqlite_product_repository import (
    SQLiteProductRepository,
)
from gestor_de_stock.infrastructure.sqlite_user_repository import SQLiteUserRepository


@pytest.fixture
def client_user(api_user_repository, rate_limiter):
    app.dependency_overrides[get_user_repository] = lambda: api_user_repository
    app.dependency_overrides[get_rate_limiter] = lambda: rate_limiter
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client_product(api_product_repository, verified_user_payload):
    app.dependency_overrides[get_product_repository] = lambda: api_product_repository
    app.dependency_overrides[get_current_user] = lambda: verified_user_payload
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def client_category(api_category_repository):
    app.dependency_overrides[get_category_repository] = lambda: api_category_repository
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def api_product_repository(connection):
    return SQLiteProductRepository(connection)


@pytest.fixture
def api_category_repository(connection):
    return SQLiteCategoryRepository(connection)


@pytest.fixture
def api_user_repository(connection):
    return SQLiteUserRepository(connection)


@pytest.fixture
def product():
    return Product(id=1, name="Test Product", price=50, quantity=10, category_id=1)


@pytest.fixture
def existing_product():
    return Product(id=2, name="Existing Product", price=30, quantity=5, category_id=1)


@pytest.fixture
def category():
    return Category(id=None, name="Test Category")


@pytest.fixture
def connection():
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price FLOAT NOT NULL,
            quantity INTEGER NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL UNIQUE,
           email TEXT NOT NULL UNIQUE,
           password_hash TEXT NOT NULL
        )
    """)
    yield connection
    connection.close()


@pytest.fixture
def create_product(api_product_repository):
    def _create_product(name="Test Product", price=50, quantity=10, category_id=1):
        product = Product(
            id=None, name=name, price=price, quantity=quantity, category_id=category_id
        )
        api_product_repository.save(product)
        return product

    return _create_product


@pytest.fixture
def create_category(api_category_repository):
    def _create_category(name="Test Category"):
        category = Category(id=None, name=name)
        api_category_repository.save(category)
        return category

    return _create_category


@pytest.fixture
def product_repository(connection):
    return SQLiteProductRepository(connection)


@pytest.fixture
def category_repository(connection):
    return SQLiteCategoryRepository(connection)


@pytest.fixture
def user_repository(connection):
    return SQLiteUserRepository(connection)


@pytest.fixture
def user():
    return User(
        id=None,
        username="Adnane",
        email="infadadnan@gmail.com",
        password_hash="fake_hashed_password",
    )


@pytest.fixture
def password_hasher():
    return PasswordHasher()


@pytest.fixture
def correct_password():
    password = "dxdiag"
    return password


@pytest.fixture
def jwt_service():
    return JWTService(secret_key="this_is_a_test_secret_key_123456", expiration_time=10)


@pytest.fixture
def rate_limiter():
    return InMemoryRateLimiter(60, 5)


@pytest.fixture
def verified_user_payload(jwt_service: JWTService):
    payload = {"user_id": 1, "username": "Adnane", "email": "infadadnan@gmail.com"}
    token = jwt_service.generate_token(payload)
    verified_payload = jwt_service.verify_token(token)
    return verified_payload
