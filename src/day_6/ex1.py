"""
ex1. 
Mock data generation
save dictionary to csv

"""


from datetime import datetime, timedelta
import random
from statistics import mean, stdev

# 1️⃣ Generate sample data (Extract & Transform)
random.seed(42)
start_date = datetime(2024, 1, 1)
data = []

for i in range(639):  # about 21 months of daily data
    date = start_date + timedelta(days=i)
    region = random.choice(["Europe", "Asia", "North America"])
    sales = round(random.gauss(50000, 8000), 2)
    marketing_spend = round(random.gauss(8000, 1000), 2)
    data.append({"date": date, "region": region, "sales": sales, "marketing_spend": marketing_spend})

print (data)
print("---------------------------------------------------------------------    ")

import csv

csv_filename = "data/daily_sales_data.csv"


from datetime import datetime, timedelta
import random
from statistics import mean, stdev
import matplotlib.pyplot as plt


# Get field names automatically from dictionary keys
fieldnames = data[0].keys()

with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


print("---------------------------------------------------------------------    ")



