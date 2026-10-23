from gestor_de_stock.infrastructure.database import database

from .domain.product import Product


class Inventory:
    def get_all_products(self):
        return database.get_all_products()

    def add_product(self, product: Product) -> Product:
        return database.insert_product(product)

    def find_product(self, id):
        return database.find_product(id)

    def remove_product(self, id) -> bool:
        return database.delete_product(id)

    def update_product(self, id, name, price, quantity, category_id):
        return database.update_product(id, name, price, quantity, category_id)
