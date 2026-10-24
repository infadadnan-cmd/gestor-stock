from gestor_de_stock.domain.product import Product
from gestor_de_stock.domain.product_with_category import ProductWithCategory
from gestor_de_stock.repositories.product_repository import ProductRepository


class SQLiteProductRepository(ProductRepository):
    def __init__(self, connection):
        self.connection = connection

    def save(self, product: Product) -> None:
        cursor = self.connection.execute(
            """
            INSERT INTO products (name, price, quantity, category_id)
            VALUES (?, ?, ?, ?)
            """,
            (product.name, product.price, product.quantity, product.category_id),
        )
        self.connection.commit()
        product.id = cursor.lastrowid

    def get_by_id(self, product_id: int) -> Product | None:
        row = self.connection.execute(
            """
            SELECT id, name, price, quantity, category_id
            FROM products
            WHERE id = ?
            """,
            (product_id,),
        ).fetchone()

        if row is None:
            return None
        return Product(
            id=row["id"],
            name=row["name"],
            price=row["price"],
            quantity=row["quantity"],
            category_id=row["category_id"],
        )

    def get_all(self) -> list[Product]:
        rows = self.connection.execute(
            """
            SELECT
            products.id,
            products.name,
            products.price,
            products.quantity,
            products.category_id,
            categories.name as category_name
            FROM products
            LEFT JOIN categories
                ON products.category_id= categories.id
            """
        ).fetchall()
        return [
            ProductWithCategory(
                id=row["id"],
                name=row["name"],
                price=row["price"],
                quantity=row["quantity"],
                category_id=row["category_id"],
                category_name=row["category_name"],
            )
            for row in rows
        ]

    def delete(self, product_id: int) -> None:
        self.connection.execute(
            """
            DELETE FROM products
            WHERE id = ?
            """,
            (product_id,),
        )
        self.connection.commit()

    def update(self, product: Product) -> Product | None:
        self.connection.execute(
            """
            UPDATE products
            SET name = ?, price = ?, quantity = ?, category_id = ?
            WHERE id = ?
            """,
            (
                product.name,
                product.price,
                product.quantity,
                product.category_id,
                product.id,
            ),
        )
        self.connection.commit()
        if self.get_by_id(product.id) is None:
            return None
        return self.get_by_id(product.id)
