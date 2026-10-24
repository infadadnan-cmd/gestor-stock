from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class SQLiteCategoryRepository(CategoryRepository):
    def __init__(self, connection):
        self.connection = connection

    def save(self, category: Category):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
        self.connection.commit()
        category.id = cursor.lastrowid

    def find_by_id(self, category_id: int):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        if row:
            return Category(id=row[0], name=row[1])
        return None

    def find_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        return [Category(id=row[0], name=row[1]) for row in rows]

    def delete(self, category_id: int):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.connection.commit()

    def update(self, category: Category):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?", (category.name, category.id)
        )
        self.connection.commit()
        if cursor.rowcount == 0:
            return None
        return category
