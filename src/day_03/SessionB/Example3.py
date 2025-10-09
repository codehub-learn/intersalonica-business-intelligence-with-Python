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


