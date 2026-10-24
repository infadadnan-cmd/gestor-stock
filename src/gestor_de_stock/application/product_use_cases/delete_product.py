from gestor_de_stock.repositories.product_repository import ProductRepository


class DeleteProduct:
    def __init__(self, productRepository: ProductRepository):
        self.productRepository = productRepository

    def execute(self, product_id: int) -> None:
        if self.productRepository.get_by_id(product_id) is None:
            raise ValueError("Product not found")
        self.productRepository.delete(product_id)
