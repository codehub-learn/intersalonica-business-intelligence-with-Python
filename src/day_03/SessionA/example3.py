"""
Dimensional Modeling (Kimball’s Approach)
Task: Implement a Star Schema with facts + dimensions.

"""

# Dimensions
dim_time = {
    1: {"date": "2025-01-01", "month": "January", "year": 2025},
    2: {"date": "2025-01-02", "month": "January", "year": 2025},
}

dim_customer = {
    1: {"name": "Alice", "region": "North"},
    2: {"name": "Bob", "region": "South"},
}

dim_product = {
    101: {"name": "Laptop", "category": "Electronics"},
    102: {"name": "Chair", "category": "Furniture"},
}

# Fact table (sales fact)
fact_sales = [
    {"time_id": 1, "cust_id": 1, "product_id": 101, "amount": 120},
    {"time_id": 2, "cust_id": 2, "product_id": 102, "amount": 200},
    {"time_id": 1, "cust_id": 1, "product_id": 102, "amount": 80},
]

# Query: Sales by category
sales_by_category = {}
for sale in fact_sales:
    product = dim_product[sale["product_id"]]
    cat = product["category"]
    sales_by_category[cat] = sales_by_category.get(cat, 0) + sale["amount"]

print("Sales by category:", sales_by_category)
