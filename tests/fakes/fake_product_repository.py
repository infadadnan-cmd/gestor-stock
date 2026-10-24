from gestor_de_stock.domain.product import Product
from gestor_de_stock.repositories.product_repository import ProductRepository


class FakeProductRepository(ProductRepository):
    def __init__(self):
        self.requested_id = None
        self.products = []

    def save(self, product: Product) -> None:
        product.id = 1
        self.products.append(product)

    def get_by_id(self, product_id: int) -> Product | None:
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_all(self) -> list[Product]:
        return self.products

    def delete(self, product_id: int) -> None:
        self.requested_id = product_id
        self.products = [
            product for product in self.products if product.id != product_id
        ]

    def update(self, product: Product) -> Product | None:
        for existing_product in self.products:
            if existing_product.id == product.id:
                existing_product.name = product.name
                existing_product.price = product.price
                existing_product.quantity = product.quantity
                existing_product.category_id = product.category_id
                updated_prodcut = existing_product
                return updated_prodcut
