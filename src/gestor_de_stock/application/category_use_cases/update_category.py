from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class UpdateCategory:
    def __init__(self, categoryRepository: CategoryRepository):
        self.categoryRepository = categoryRepository

    def execute(self, category: Category) -> Category | None:
        return self.categoryRepository.update(category)
