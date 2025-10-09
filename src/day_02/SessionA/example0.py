
#######################################################
sales = [1200, 500, 800, 1500, 700]

# Total sales
total = sum(sales)

# Average sale
avg = total / len(sales)

# Max sale
highest = max(sales)

print(f"Total: {total}, Average: {avg}, Highest Sale: {highest}")
print("-"*30)
print("")
#######################################################

products = [
    {"Product": "Laptop", "Revenue": 1200, "Cost": 800},
    {"Product": "Tablet", "Revenue": 500, "Cost": 300},
    {"Product": "Phone", "Revenue": 800, "Cost": 700}
]

# Add Profit and Margin
for i, p in enumerate(products):
    p["Profit"] = p["Revenue"] - p["Cost"]
    p["Margin"] = round((p["Profit"] / p["Revenue"]) * 100, 2)
    print(f"{i+1}. {p['Product']} - Profit: {p['Profit']}, Margin: {p['Margin']}%") 

print("-"*30)

# Filter low-margin products
low_margin = [p for p in products if p["Margin"] < 30]

print("Low Margin Products:", low_margin)
#######################################################

