from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=3, max_length=100)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str


class OrderItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=32)
    quantity: int = Field(ge=1)
    price: int = Field(ge=0)


class OrderCreate(BaseModel):
    order_no: str = Field(min_length=1, max_length=32)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    sku: str
    quantity: int
    price: int


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    status: str
    total_amount: int
    idempotency_key: str
    items: list[OrderItemResponse]
