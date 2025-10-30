"""
ex2.py -

Advanced Data Analysis and Visualization

This script processes daily sales data to compute monthly KPIs, detect anomalies,
perform a simple sales forecast, and create visualizations using Matplotlib.
"""




from datetime import datetime, timedelta
import random
from statistics import mean, stdev
import matplotlib.pyplot as plt



import csv

csv_filename = "data/daily_sales_data.csv"


#read data from csv as list of dictionaries
data = []   

with open(csv_filename, mode="r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        #convert date string to datetime object
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
        #convert sales and marketing_spend to float
        row["sales"] = float(row["sales"])
        row["marketing_spend"] = float(row["marketing_spend"])
        data.append(row)


# Helper: get month string like '2024-03'
def month_key(date):
    return f"{date.year}-{date.month:02d}"


################################################################################################################################

# 2️⃣ Aggregate Monthly KPIs
monthly = {}
for entry in data:
    month = month_key(entry["date"])
    if month not in monthly:
        monthly[month] = {"sales": 0, "marketing_spend": 0}
    monthly[month]["sales"] += entry["sales"]
    monthly[month]["marketing_spend"] += entry["marketing_spend"]

# Calculate ROI and detect anomalies
months = sorted(monthly.keys())
roi_values = []

for m in months:
    s = monthly[m]["sales"]
    sp = monthly[m]["marketing_spend"]
    roi = (s - sp) / sp if sp else 0
    monthly[m]["roi"] = roi
    roi_values.append(roi)

mean_roi = mean(roi_values)
stdev_roi = stdev(roi_values)
threshold = mean_roi - 2 * stdev_roi

for m in months:
    monthly[m]["anomaly"] = "Yes" if monthly[m]["roi"] < threshold else "No"

################################################################################################################################





# 3️⃣ Simple Forecast (Predictive Logic)
if len(months) >= 2:
    last_sales = monthly[months[-1]]["sales"]
    prev_sales = monthly[months[-2]]["sales"]
    growth_rate = (last_sales - prev_sales) / prev_sales if prev_sales else 0
    predicted_sales = last_sales * (1 + growth_rate)
else:
    predicted_sales = 0

print(f"Predicted next month sales: ${predicted_sales:,.2f}")

# Prepare data for plotting
sales = [monthly[m]["sales"] for m in months]
roi = [monthly[m]["roi"] for m in months]
spend = [monthly[m]["marketing_spend"] for m in months]
anomaly_flags = [monthly[m]["anomaly"] == "Yes" for m in months]

################################################################################################################################

# 4️⃣ Visualization (Matplotlib)

plt.figure(figsize=(12, 8))

# ---- Chart 1: Sales Trend ----
plt.subplot(3, 1, 1)
plt.plot(months, sales, marker='o', color='tab:blue')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True)

# ---- Chart 2: ROI with Anomalies ----
plt.subplot(3, 1, 2)
colors = ['red' if a else 'green' for a in anomaly_flags]
plt.bar(months, roi, color=colors)
plt.axhline(y=threshold, color='orange', linestyle='--', label='Anomaly Threshold')
plt.title("ROI with Anomaly Detection")
plt.xlabel("Month")
plt.ylabel("ROI")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, axis='y')

# ---- Chart 3: Marketing Spend vs Sales ----
plt.subplot(3, 1, 3)
plt.scatter(spend, sales, s=[r * 300 for r in roi], c=roi, cmap='viridis', alpha=0.7)
plt.colorbar(label="ROI")
plt.title("Marketing Spend vs Sales")
plt.xlabel("Marketing Spend")
plt.ylabel("Sales")
plt.grid(True)

plt.tight_layout()
plt.show()
