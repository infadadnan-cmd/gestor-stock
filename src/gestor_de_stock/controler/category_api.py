from fastapi import APIRouter, Depends, HTTPException, status

from gestor_de_stock.application.category_use_cases.create_category import (
    CreateCategory,
)
from gestor_de_stock.application.category_use_cases.delete_category import (
    DeleteCategory,
)
from gestor_de_stock.application.category_use_cases.get_categories import GetCategories
from gestor_de_stock.application.category_use_cases.get_category import GetCategory
from gestor_de_stock.application.category_use_cases.update_category import (
    UpdateCategory,
)
from gestor_de_stock.domain.category import Category
from gestor_de_stock.infrastructure.database import connection
from gestor_de_stock.infrastructure.sqlite_category_repository import (
    SQLiteCategoryRepository,
)
from gestor_de_stock.shemas import CategoryCreate, CategoryResponse

router = APIRouter()


def get_category_repository():
    return SQLiteCategoryRepository(connection)


@router.get("/categories", response_model=list[CategoryCreate])
def get_categories(
    categoryRepository=Depends(get_category_repository),
) -> list[CategoryCreate]:
    get_categories_use_case = GetCategories(categoryRepository)

    categories = get_categories_use_case.execute()

    return categories


@router.get("/categories/{id}", response_model=CategoryResponse)
def get_category(id: int, categoryRepository=Depends(get_category_repository)):
    get_category_use_case = GetCategory(categoryRepository)
    category = get_category_use_case.execute(id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate, categoryRepository=Depends(get_category_repository)
):
    create_category_use_case = CreateCategory(categoryRepository)
    created_category = create_category_use_case.execute(name=category.name)

    return created_category


@router.put("/categories/{id}")
def update_category(
    id: int,
    category: CategoryCreate,
    categoryRepository=Depends(get_category_repository),
):
    use_case = UpdateCategory(categoryRepository)
    category_to_update = Category(id=id, name=category.name)

    updated_category = use_case.execute(category_to_update)

    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category


@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, categoryRepository=Depends(get_category_repository)):
    delete_category_use_case = DeleteCategory(categoryRepository)
    delete_category_use_case.execute(id)
