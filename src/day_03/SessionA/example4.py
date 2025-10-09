"""
Inmon’s Approach (Normalized DW)

Task: Simulate a normalized warehouse (3NF) and query it.
"""

# Normalized tables (Inmon style)
customers = [
    {"cust_id": 1, "name": "Alice", "region": "North"},
    {"cust_id": 2, "name": "Bob", "region": "South"},
]

products = [
    {"prod_id": 101, "name": "Laptop", "category": "Electronics"},
    {"prod_id": 102, "name": "Chair", "category": "Furniture"},
]

sales = [
    {"sale_id": 1, "cust_id": 1, "prod_id": 101, "amount": 120},
    {"sale_id": 2, "cust_id": 2, "prod_id": 102, "amount": 200},
    {"sale_id": 3, "cust_id": 1, "prod_id": 102, "amount": 80},
]

# Query: Join tables to get full info
for s in sales:
    cust = next(c for c in customers if c["cust_id"] == s["cust_id"])
    prod = next(p for p in products if p["prod_id"] == s["prod_id"])
    print(f"{cust['name']} from {cust['region']} bought {prod['name']} ({prod['category']}) for {s['amount']}")
