from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from .db import engine, create_db_and_tables
from .models import Order, OrderCreate, OrderRead, Inventory

app = FastAPI(title="Coffee Shop API")


MENU = [
    {"id": 1, "name": "Americano", "price": 3.5},
    {"id": 2, "name": "Latte", "price": 4.5},
    {"id": 3, "name": "Cappuccino", "price": 4.2},
]


@app.on_event("startup")
def startup():
    create_db_and_tables()

    with Session(engine) as session:
        if not session.exec(select(Inventory)).first():
            for m in MENU:
                session.add(Inventory(item_id=m["id"], stock=10))
            session.commit()


@app.get("/api/menu")
def get_menu():
    return MENU


@app.get("/api/orders", response_model=list[OrderRead])
def list_orders():
    with Session(engine) as session:
        return session.exec(select(Order)).all()


@app.post("/api/orders", response_model=OrderRead)
def create_order(order: OrderCreate):
    with Session(engine) as session:

        inventory = session.get(Inventory, order.item_id)

        if inventory.stock < order.qty:
            raise HTTPException(
                status_code=409,
                detail="Not enough stock"
            )

        inventory.stock -= order.qty

        db_order = Order(**order.model_dump())

        session.add(db_order)
        session.commit()
        session.refresh(db_order)

        return db_order