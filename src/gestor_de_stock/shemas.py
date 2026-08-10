from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)
