from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class GetCategories:
    def __init__(self, categoryRepository: CategoryRepository):
        self.categoryRepository = categoryRepository

    def execute(self) -> list[Category]:
        return self.categoryRepository.find_all()
