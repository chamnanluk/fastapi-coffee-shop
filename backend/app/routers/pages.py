from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
def customer_page(request: Request):
    return templates.TemplateResponse("customer.html", {"request": request})

@router.get("/kitchen", response_class=HTMLResponse)
def kitchen_page(request: Request):
    return templates.TemplateResponse("kitchen.html", {"request": request})
