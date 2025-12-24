from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str | None = None
    stock: int = Field(ge=0)
    price: float = Field(ge=0)

class ProductOut(BaseModel):
    id: int
    name: str
    category: str | None
    stock: int
    price: float

    class Config:
        from_attributes = True