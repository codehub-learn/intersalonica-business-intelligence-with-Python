import json

# Example business sales data in JSON format
sales_data_json = """
[
    {"Product": "Laptop", "Revenue": 1200, "Cost": 800},
    {"Product": "Tablet", "Revenue": 500, "Cost": 300},
    {"Product": "Phone", "Revenue": 800, "Cost": 700},
    {"Product": "Monitor", "Revenue": 400, "Cost": 250}
]
"""



# Convert JSON string into Python objects
sales_data = json.loads(sales_data_json)

# Add Profit and Margin for BI analysis
for item in sales_data:
    item["Profit"] = item["Revenue"] - item["Cost"]
    item["Margin %"] = round((item["Profit"] / item["Revenue"]) * 100, 2)

print(sales_data)


# Save enriched data into a new JSON file
with open("data/sales_report.json", "w") as f:
    json.dump(sales_data, f, indent=4)

print("✅ Sales report saved to sales_report.json")



# Load and display the saved report
with open("data/sales_report.json", "r") as f:
    report = json.load(f)
    for item in report:
        print(f"Product: {item['Product']}, Revenue: {item['Revenue']}, Cost: {item['Cost']}, Profit: {item['Profit']}, Margin: {item['Margin %']}%")       
        