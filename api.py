from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, status

from inventory import Inventory
from product import Product

inventory= Inventory()
app = FastAPI()
from shemas import ProductResponse, ProductCreate 


@app.get("/")
def home():
    return {"message": "API running"}


@app.get("/products", response_model=list[ProductResponse])
def get_products() -> list[ProductResponse]:
    products= inventory.get_all_products()
    return [ProductResponse.model_validate(product)
    for product in products
    ]
@app.get("/products/{id}", response_model= ProductResponse)
def get_product(id: int):
    product= inventory.find_product(id)
    if not product:
             raise HTTPException(
                    status_code=404,
                    detail= "Product not found"
                )
    return ProductResponse.model_validate(product)



@app.post("/products", status_code= status.HTTP_201_CREATED)
def create_product(product: ProductCreate):

    new_product = Product(
        name= product.name,
        price= product.price
    )
    created_product = inventory.add_product(new_product)

    return ProductResponse.model_validate(created_product)

@app.delete("/products/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_product(id):
    if inventory.remove_product(id):
        return None
    raise HTTPException(
        status_code=404,
        detail= "Product not found"
    )
@app.put("/products/{id}")
def update_product(id: int, product: ProductCreate):
    if not inventory.find_product(id):
         raise HTTPException(
                status_code=404,
                detail= "Product not found"
            )
    inventory.update_product(
        id,
        product.name,
        product.price
    )
    updated_product= inventory.find_product(id)
    return ProductResponse.model_validate(updated_product)
    
    

