from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class OrderStatus(str, Enum):
    RECEIVED = "RECEIVED"
    PREPARING = "PREPARING"
    READY = "READY"
    CANCELLED = "CANCELLED"


class OrderBase(SQLModel):
    customer_name: str
    item_id: int
    qty: int
    note: Optional[str] = None


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
