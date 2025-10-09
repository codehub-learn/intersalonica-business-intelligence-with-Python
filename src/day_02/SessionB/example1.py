import csv

#load sales data from CSV and print each row
with open("data/sales.csv", "r") as file:
    reader = csv.DictReader(file)
    sales_data = []
    for row in reader:
        sales_data.append(row)
        print(f"Product: {row['Product']}, Revenue: {row['Revenue']}, Cost: {row['Cost']}")

print(sales_data)
print("-"*30)

#save sales data to CSV
with open("data/output_sales.csv", "w", newline='') as file:
    fieldnames = ["Product", "Revenue", "Cost"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"Product": "Laptop", "Revenue": 1200, "Cost": 800})
    writer.writerow({"Product": "Tablet", "Revenue": 500, "Cost": 300}) 

print("✅ Sales data saved to output_sales.csv")
