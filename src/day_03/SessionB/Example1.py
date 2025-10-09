"""

Fact Tables for Measurements
A fact table stores numeric measurements (sales, revenue, etc.) linked to dimensions.


Create a fact table in Python as a list of dictionaries for sales transactions:
"""

fact_sales = [
    {"sale_id": 1, "product_id": 101, "customer_id": 201, "date_id": 301, "quantity": 2, "amount": 50.0},
    {"sale_id": 2, "product_id": 102, "customer_id": 202, "date_id": 302, "quantity": 1, "amount": 20.0},
    {"sale_id": 3, "product_id": 103, "customer_id": 201, "date_id": 303, "quantity": 3, "amount": 75.0},
]
# Print the fact table
for record in fact_sales:
    print(record)   

"""
Dimension Tables for Descriptive Context

A dimension table provides descriptive attributes for facts (e.g., product details, customer demographics).

Create dimension tables in Python:
"""


dim_product = {
    101: {"name": "Laptop", "category": "Electronics"},
    102: {"name": "Shirt", "category": "Clothing"},
    103: {"name": "Book", "category": "Education"}
}

dim_customer = {
    201: {"name": "Alice", "region": "North"},
    202: {"name": "Bob", "region": "South"}
}

dim_date = {
    301: {"date": "2025-10-01", "day": "Wednesday", "month": "October"},
    302: {"date": "2025-10-02", "day": "Thursday", "month": "October"},
    303: {"date": "2025-10-03", "day": "Friday", "month": "October"}
}
   
"""
Facts and Dimensions Joined in a Star Schema

A star schema links fact tables to multiple dimensions.

Exercise 3:
Use fact_sales, dim_product, dim_customer, and dim_date.
"""


"""
Alice bought Laptop (Electronics) on 2025-10-01 for $50.0
Bob bought Shirt (Clothing) on 2025-10-02 for $20.0
Alice bought Book (Education) on 2025-10-03 for $75.0

"""

"""
Fact measurements → numbers
Dimension descriptions → context
Star schema joins → reports
Schema variations → star, snowflake, galaxy

"""