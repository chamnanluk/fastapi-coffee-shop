from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from .db import create_db_and_tables, engine
from .models import Inventory, Order, OrderCreate, OrderRead, OrderStatusUpdate

app = FastAPI(title="Coffee Shop API", version="1.0.0")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

MENU = [
    {"id": 1, "name": "Americano", "price": 3.5},
    {"id": 2, "name": "Latte", "price": 4.5},
    {"id": 3, "name": "Cappuccino", "price": 4.2},
]
MENU_BY_ID = {item["id"]: item for item in MENU}


@app.on_event("startup")
def startup() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        if not session.exec(select(Inventory)).first():
            for item in MENU:
                session.add(Inventory(item_id=item["id"], stock=10))
            session.commit()


@app.get("/", response_class=HTMLResponse)
def customer_page(request: Request):
    return templates.TemplateResponse("customer.html", {"request": request})


@app.get("/kitchen", response_class=HTMLResponse)
def kitchen_page(request: Request):
    return templates.TemplateResponse("kitchen.html", {"request": request})


@app.get("/api/menu")
def get_menu():
    return MENU


@app.get("/api/inventory")
def get_inventory():
    with Session(engine) as session:
        inventory_rows = session.exec(select(Inventory)).all()

    result = []
    for row in inventory_rows:
        item = MENU_BY_ID.get(row.item_id)
        result.append(
            {
                "item_id": row.item_id,
                "item_name": item["name"] if item else "Unknown",
                "stock": row.stock,
            }
        )
    return result


@app.get("/api/orders", response_model=list[OrderRead])
def list_orders():
    with Session(engine) as session:
        return session.exec(select(Order).order_by(Order.id.desc())).all()


@app.post("/api/orders", response_model=OrderRead)
def create_order(order: OrderCreate):
    if order.item_id not in MENU_BY_ID:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if order.qty <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be more than 0")

    with Session(engine) as session:
        inventory = session.get(Inventory, order.item_id)
        if inventory is None:
            raise HTTPException(status_code=404, detail="Inventory item missing")

        if inventory.stock < order.qty:
            raise HTTPException(status_code=409, detail="Not enough stock")

        inventory.stock -= order.qty

        db_order = Order(**order.model_dump())
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order


@app.patch("/api/orders/{order_id}/status", response_model=OrderRead)
def update_order_status(order_id: int, payload: OrderStatusUpdate):

    with Session(engine) as session:
        order = session.get(Order, order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = payload.status
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
