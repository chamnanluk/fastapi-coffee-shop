from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from .db import create_db_and_tables, engine
from .models import Inventory
from .config import MENU
from .routers import api, pages

app = FastAPI(title="Coffee Shop API", version="1.0.0")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Include Routers
app.include_router(pages.router)
app.include_router(api.router)


# @app.on_event("startup")
# def startup() -> None:
#     create_db_and_tables()

#     with Session(engine) as session:
#         for item in MENU:
#             inventory_item = session.get(Inventory, item["id"])
#             if not inventory_item:
#                 session.add(Inventory(item_id=item["id"], stock=10))
#         session.commit()

# new version
@app.on_event("startup")
def startup() -> None:
    create_db_and_tables()

    with Session(engine) as session:
        for item in MENU:
            inventory_item = session.get(Inventory, item["id"])
            if not inventory_item:
                # Update this line below:
                session.add(Inventory(item_id=item["id"], stock=item["stock"]))
        session.commit()
