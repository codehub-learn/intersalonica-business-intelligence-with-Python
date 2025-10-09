"""
Simulation of different DW components (ETL, staging, data warehouse, data marts).

Task Simulate "raw data" (OLTP system)

"""



transactions = [
    {"txn_id": 1, "customer": "Alice", "amount": 120, "region": "North"},
    {"txn_id": 2, "customer": "Bob", "amount": 200, "region": "South"},
    {"txn_id": 3, "customer": "Alice", "amount": 150, "region": "North"},
    {"txn_id": 4, "customer": "Alice", "amount": 0, "region": "North"},
]

# 1. Staging area (cleaning)
staging = [t for t in transactions if t["amount"] > 0]

# 2. Load into "Data Warehouse" fact table
fact_sales = [{"customer": t["customer"], "amount": t["amount"]} for t in staging]

# 3. Create a Data Mart (regional sales summary)
mart_sales_by_region = {}
for t in staging:
    mart_sales_by_region[t["region"]] = mart_sales_by_region.get(t["region"], 0) + t["amount"]



# Output results
print("Staging area:", staging)
print("-"*40)
print("Fact table:", fact_sales)
print("-"*40)
print("Sales by region mart:", mart_sales_by_region)
