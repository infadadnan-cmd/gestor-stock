from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: int = Field(gt=0)
    quantity: int = Field(gt=0)
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    quantity: int
    category_id: int | None = None
    category_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    password: str = Field(min_length=12)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
