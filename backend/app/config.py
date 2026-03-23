MENU = [
    {"id": 1, "name": "Americano", "price": 3.5, "stock": 100},
    {"id": 2, "name": "Latte", "price": 4.5, "stock": 15},
    {"id": 3, "name": "Cappuccino", "price": 4.2, "stock": 30},
# Add your new item below! 
# Make sure the ID is unique (4) and add a comma on the line above
    {"id": 4, "name": "Mocha", "price": 5.0, "stock": 20},
]

MENU_BY_ID = {item["id"]: item for item in MENU}
