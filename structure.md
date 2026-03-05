# Project Structure (FastAPI Coffee Shop)

```text
fastapi-coffee-shop
│
├── backend
│   ├── app
│   │   ├── main.py        # FastAPI app, HTML routes, API routes
│   │   ├── db.py          # SQLite engine + table creation
│   │   └── models.py      # SQLModel schemas and tables
│   ├── templates
│   │   ├── customer.html  # Customer ordering page
│   │   └── kitchen.html   # Kitchen dashboard page
│   ├── static
│   │   └── coffee.css     # Shared styling
│   └── requirements.txt
│
├── docs
│   └── architecture.md
├── run.sh
├── README.md
└── structure.md
```

## Learning flow
1. Open `/` to place orders from a customer view.
2. Open `/kitchen` to manage order status and inspect inventory.
3. Open `/docs` to explore FastAPI's auto-generated OpenAPI docs.
