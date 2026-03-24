from enum import Enum
from typing import Optional
from pydantic import validator

from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PREPARING = "PREPARING"
    READY = "READY"
    CANCELLED = "CANCELLED"


# class OrderBase(SQLModel):
#     customer_name: str
#     item_id: int
#     qty: int
#     note: Optional[str] = None

# class OrderBase(SQLModel):
#     # Strip whitespace, require at least 1 char, limit to 100 chars
#     customer_name: str = Field(min_length=1, max_length=100)
    
#     item_id: int
    
#     # Must be greater than 0, upper bound optional but recommended (e.g., max 50)
#     qty: int = Field(gt=0, le=50)
    
#     note: Optional[str] = None

class OrderBase(SQLModel):
    customer_name: str = Field(min_length=1, max_length=100)
    item_id: int
    qty: int = Field(gt=0, le=50)
    note: Optional[str] = None

    @validator("customer_name")
    def customer_name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("customer_name cannot be empty or just whitespace")
        return v.strip()

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: OrderStatus = Field(default=OrderStatus.RECEIVED)


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    status: OrderStatus


class OrderStatusUpdate(SQLModel):
    status: OrderStatus


class Inventory(SQLModel, table=True):
    item_id: int = Field(primary_key=True)
    stock: int = 0

class InventoryUpdate(SQLModel):
    # Must be greater than 0 (rejects 0 and negative numbers)
    add_stock: int = Field(gt=0)

# class InventoryUpdate(SQLModel):
#     add_stock: int
