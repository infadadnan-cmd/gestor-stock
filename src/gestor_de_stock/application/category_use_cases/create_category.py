from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class CreateCategory:
    def __init__(self, categoryRepository: CategoryRepository):
        self.categoryRepository = categoryRepository

    def execute(self, name: str) -> Category:
        category = Category(id=None, name=name)
        self.categoryRepository.save(category)
        return category
