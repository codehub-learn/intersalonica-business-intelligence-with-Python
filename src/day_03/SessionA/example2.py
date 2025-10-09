"""
# Separate fact data from dimension data.
Task: Join fact and dimension tables to get enriched info.

"""




# Dimension tables
dim_customer = {
    1: {"name": "Alice", "region": "North"},
    2: {"name": "Bob", "region": "South"},
}

dim_product = {
    101: {"product": "Laptop", "category": "Electronics"},
    102: {"product": "Chair", "category": "Furniture"},
}

# Fact table
fact_sales = [
    {"txn_id": 1, "cust_id": 1, "product_id": 101, "amount": 120},
    {"txn_id": 2, "cust_id": 2, "product_id": 102, "amount": 200},
    {"txn_id": 3, "cust_id": 1, "product_id": 101, "amount": 150},
]

# Join fact with dimensions (like a star schema query)
for sale in fact_sales:
    customer = dim_customer[sale["cust_id"]]
    product = dim_product[sale["product_id"]]
    print(f"Customer {customer['name']} from {customer['region']} bought {product['product']} for {sale['amount']}")
