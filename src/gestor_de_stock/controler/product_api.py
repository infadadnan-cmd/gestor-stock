from fastapi import Depends, FastAPI, HTTPException, status

from gestor_de_stock.application.product_use_cases.delete_product import DeleteProduct
from gestor_de_stock.application.product_use_cases.get_product import GetProduct
from gestor_de_stock.application.product_use_cases.get_products import GetProducts
from gestor_de_stock.application.product_use_cases.update_product import UpdateProduct
from gestor_de_stock.controler.category_api import router as category_router
from gestor_de_stock.controler.user_api import router as user_router
from gestor_de_stock.domain.product import Product
from gestor_de_stock.infrastructure.database import connection
from gestor_de_stock.infrastructure.security.dependencies import get_current_user

from ..application.product_use_cases.create_product import CreateProduct
from ..infrastructure.sqlite_product_repository import SQLiteProductRepository
from ..shemas import ProductCreate, ProductResponse

app = FastAPI()
app.include_router(category_router)
app.include_router(user_router)
productRepository = SQLiteProductRepository(connection)
create_product_use_case = CreateProduct(productRepository)
get_products_use_case = GetProducts(productRepository)


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


def get_product_repository():
    return SQLiteProductRepository(connection)


@app.get("/")
def home():
    return {"message": "API running"}


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    productRepository=Depends(get_product_repository),
    current_user=Depends(get_current_user),
) -> list[ProductResponse]:

    use_case = GetProducts(productRepository)

    products = use_case.execute()

    return [ProductResponse.model_validate(product) for product in products]


@app.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int, productRepository=Depends(get_product_repository)):
    get_product_use_case = GetProduct(productRepository)
    product = get_product_use_case.execute(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.model_validate(product)


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, productRepository=Depends(get_product_repository)
):
    create_product_use_case = CreateProduct(productRepository)
    created_product = create_product_use_case.execute(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )

    return ProductResponse.model_validate(created_product)


@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, productRepository=Depends(get_product_repository)):
    delete_product_use_case = DeleteProduct(productRepository)
    try:
        delete_product_use_case.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/products/{id}")
def update_product(
    id: int, product: ProductCreate, productRepository=Depends(get_product_repository)
):
    existing_product = productRepository.get_by_id(id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = Product(
        id=id,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        category_id=product.category_id,
    )

    use_case = UpdateProduct(productRepository)
    try:
        updated_product = use_case.execute(updated_product)
        return ProductResponse.model_validate(updated_product)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
