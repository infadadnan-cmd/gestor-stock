import os
import sqlite3
from .product import Product

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DB_PATH = os.path.join(BASE_DIR, "Inventory.db")

connection = sqlite3.connect(DB_PATH, check_same_thread=False)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
def create_table():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, 
    price INTEGER
    
    )
    """)
    connection.commit()
def insert_product(product):
    cursor.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (product.name, product.price)
    )

    print("LASTROWID:", cursor.lastrowid)

    connection.commit()

    new_product = Product(
        id=cursor.lastrowid,
        name=product.name,
        price=product.price
    )

    print("NEW PRODUCT:", new_product.__dict__)

    return new_product
def get_all_products() -> list[Product]: 
    cursor.execute(
        "SELECT id, name, price FROM products"
        )

    rows = cursor.fetchall()
    connection.commit()
    return [Product.from_row(row) for row in rows]

def find_product(id) -> Product | None: 
    cursor.execute("SELECT id, name, price FROM products WHERE id=?", (id,)
                   )
    row= cursor.fetchone()
    if row is not None:
        return Product.from_row(row)
    return None
def update_product(id, name, price):
    cursor.execute(
        """ 
        UPDATE products
        SET name= ?,
        price= ?
        WHERE id= ?
        """,
        (name, price, id)
    )
    connection.commit()
    return cursor.rowcount> 0

def delete_product(id):
    cursor.execute(
        """ 
        DELETE FROM products
        WHERE id= ?
        """,
        (id,)
    )
    connection.commit()
    return cursor.rowcount> 0
