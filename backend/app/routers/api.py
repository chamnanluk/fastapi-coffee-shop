from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import Inventory, Order, OrderCreate, OrderRead, OrderStatusUpdate, InventoryUpdate
from ..config import MENU, MENU_BY_ID

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/menu")
def get_menu():
    return MENU

@router.get("/inventory")
def get_inventory(session: Session = Depends(get_session)):
    inventory_rows = session.exec(select(Inventory)).all()
    
    result = []
    for row in inventory_rows:
        item = MENU_BY_ID.get(row.item_id)
        result.append({
            "item_id": row.item_id,
            "item_name": item["name"] if item else "Unknown",
            "stock": row.stock,
        })
    return result

@router.get("/orders", response_model=list[OrderRead])
def list_orders(session: Session = Depends(get_session)):
    return session.exec(select(Order).order_by(Order.id.desc())).all()

@router.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    if order.item_id not in MENU_BY_ID:
        raise HTTPException(status_code=404, detail="Menu item not found")

    if order.qty <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be more than 0")

    inventory = session.get(Inventory, order.item_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item missing")

    # if inventory.stock < order.qty:
    #     raise HTTPException(status_code=409, detail="Not enough stock")
    
    if inventory.stock < order.qty:
        raise HTTPException(
            status_code=409, 
            detail=f"Not enough stock! We only have {inventory.stock} left."
        )

    inventory.stock -= order.qty

    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

# @router.patch("/orders/{order_id}/status", response_model=OrderRead)
# def update_order_status(order_id: int, payload: OrderStatusUpdate, session: Session = Depends(get_session)):
#     order = session.get(Order, order_id)
#     if order is None:
#         raise HTTPException(status_code=404, detail="Order not found")

#     order.status = payload.status
#     session.add(order)
#     session.commit()
#     session.refresh(order)
#     return order

@router.patch("/inventory/{item_id}/add-stock")
def add_to_inventory(item_id: int, payload: InventoryUpdate, session: Session = Depends(get_session)):
    # 1. Look for the item in the database
    inventory = session.get(Inventory, item_id)
    
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item missing")

    # 2. Add the requested baking amount to whatever is already there!
    inventory.stock += payload.add_stock
    
    # 3. Save it securely back into the database
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    
    return {
        "message": f"Successfully added {payload.add_stock} to stock!",
        "new_total": inventory.stock
    
    }