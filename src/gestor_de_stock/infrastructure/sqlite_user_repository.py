import sqlite3

from gestor_de_stock.domain.user import User
from gestor_de_stock.repositories.user_repository import UserRepository


class SQLiteUserRepository(UserRepository):
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def save(self, user: User) -> User:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?,?,?)
            """,
            (user.username, user.email, user.password_hash),
        )

        self.connection.commit()

        user.id = cursor.lastrowid

        return user

    def get_by_email(self, user_email: str) -> User | None:
        row = self.connection.execute(
            """ SELECT id, username, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (user_email,),
        ).fetchone()

        if row is None:
            return None

        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
        )
