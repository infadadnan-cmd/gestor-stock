from gestor_de_stock.domain.category import Category
from gestor_de_stock.repositories.category_repository import CategoryRepository


class FakeCategoryRepository(CategoryRepository):
    def __init__(self):
        self.requested_id = None
        self.categories = []

    def save(self, category: Category) -> None:
        category.id = 1
        self.categories.append(category)

    def find_by_id(self, category_id: int) -> Category | None:
        for category in self.categories:
            if category.id == category_id:
                return category
        return None

    def find_all(self) -> list[Category]:
        return self.categories

    def delete(self, category_id: int) -> None:
        self.requested_id = category_id
        self.categories = [
            category for category in self.categories if category.id != category_id
        ]

    def update(self, category: Category) -> Category | None:
        for i, existing_category in enumerate(self.categories):
            if existing_category.id == category.id:
                self.categories[i] = category
                return category
        return None
