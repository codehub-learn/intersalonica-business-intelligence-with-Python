"""
author: DI
filename: sr/day_05/tellStory.py
Description:
Date: 2025-10-23

"""


transactions = [
    {"txn_id": 1, "customer": "Alice", "amount": 120, "region": "North"},
    {"txn_id": 2, "customer": "Bob", "amount": 200, "region": "South"},
    {"txn_id": 3, "customer": "Alice", "amount": 150, "region": "North"},
    {"txn_id": 4, "customer": "Alice", "amount": 0, "region": "North"},
]

# calculate kpis for the transactions
total_sales = sum(t["amount"] for t in transactions)
average_sale = total_sales / len(transactions)
max_sale = max(t["amount"] for t in transactions)
min_sale = min(t["amount"] for t in transactions)   

sales_by_customer = {}
for t in transactions:  
    sales_by_customer[t["customer"]] = sales_by_customer.get(t["customer"], 0) + t["amount"]        



filename = "output/kpi_report.txt"
# save results to a file
with open(filename, "w") as f:   
    f.write(f"Total Sales: {total_sales}\n")
    f.write(f"Average Sale: {average_sale}\n")
    f.write(f"Max Sale: {max_sale}\n")
    f.write(f"Min Sale: {min_sale}\n")
    f.write("Sales by Customer:\n")
    for customer, amount in sales_by_customer.items():
        f.write(f"  {customer}: {amount}\n")
print("KPI report generated: kpi_report.txt")   

print("KPI calculation completed.")

#create histogram of sales amounts
import matplotlib.pyplot as plt
amounts = [t["amount"] for t in transactions]
plt.hist(amounts, bins=5, edgecolor='black')

plt.title("Sales Amount Distribution")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.show()
    
# create a pie plot of sales per region
# aggregate sales by region

sales_by_region = {}
for t in transactions:
    sales_by_region[t["region"]] = sales_by_region.get(t["region"], 0) + t["amount"]    
regions = list(sales_by_region.keys())
amounts = list(sales_by_region.values())
plt.pie(amounts, labels=regions, autopct='%1.1f%%', startangle=140)
plt.title("Sales Distribution by Region")
plt.show()
    
        