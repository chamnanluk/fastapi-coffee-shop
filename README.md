# FastAPI Coffee Shop ☕

A small learning project for understanding how APIs work in a real product flow.

## What you can learn
- Build API endpoints with FastAPI.
- Connect API + database (SQLite via SQLModel).
- Render web pages (Jinja templates).
- Use one app for two roles:
  - Customer page to create orders.
  - Kitchen dashboard to update status and monitor stock.

## Features
- Customer ordering website (`/`)
- Kitchen dashboard (`/kitchen`)
- Inventory system with stock validation
- Order status workflow (`RECEIVED`, `PREPARING`, `READY`, `CANCELLED`)
- Auto API docs (`/docs`)

## Run
```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

## Open in browser
- Customer page: http://127.0.0.1:8000/
- Kitchen page: http://127.0.0.1:8000/kitchen
- API docs: http://127.0.0.1:8000/docs
