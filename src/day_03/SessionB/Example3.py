"""
Grouping and binning
 
"""

#Grouping 
from collections import defaultdict

# Example dataset: (Customer, Product, Amount)
sales = [
    ("Alice", "iPhone", 1200),
    ("Bob", "MacBook", 2500),
    ("Alice", "Samsung", 900),
    ("Bob", "Dell", 2000),
    ("Charlie", "iPhone", 1100)
]

# Group by customer
grouped = defaultdict(list)
for customer, product, amount in sales:
    grouped[customer].append((product, amount))

# Print groups
for customer, items in grouped.items():
    total = sum(a for _, a in items)
    print(f"{customer}: purchases={items}, total={total}")

print("-----------------------")

print("Binning example:")
# Binning amounts into ranges
bins = {"<1000": 0, "1000-2000": 0, ">2000": 0}
for _, _, amount in sales:      
    if amount < 1000:
        bins["<1000"] += 1
    elif amount <= 2000:
        bins["1000-2000"] += 1
    else:
        bins[">2000"] += 1  
print("Amount bins:", bins)


print("-----------------------")
print("KPI calculation example:")
# KPI: Average sales amount per customer
customer_totals = defaultdict(int)
customer_counts = defaultdict(int) 
reference_sales = 2000  # To avoid modifying the original list
for customer, _, amount in sales:
    customer_totals[customer] += amount
    customer_counts[customer] += 1
kpis = {customer: customer_totals[customer] / customer_counts[customer]/2000 for customer in customer_totals}
print("Kpi sales per customer:", kpis)
# Output:
# Alice: purchases=[('iPhone', 1200), ('Samsung', 900)], total=2100
# Bob: purchases=[('MacBook', 2500), ('Dell', 2000)], total=4500
# Charlie: purchases=[('iPhone', 1100)], total=1100     
#  

