""""
ex4.py -    
Advanced Visualization: Heatmap of Sales Data
This script generates synthetic sales data across regions and products,
aggregates it, and visualizes it as a heatmap using Matplotlib.

"""

import matplotlib.pyplot as plt
import random
import math

# -----------------------------
# 1. Generate Synthetic Business Data
# -----------------------------
regions = ["North America", "Europe", "Asia", "South America"]
products = ["Laptops", "Smartphones", "Accessories", "Servers", "Software"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# data[region][product][quarter] = sales in USD
data = {}
for region in regions:
    data[region] = {}
    for product in products:
        q_sales = []
        for q in quarters:
            base = random.randint(80000, 150000)
            seasonal_factor = 1 + 0.1 * math.sin((quarters.index(q) + 1) * math.pi / 2)
            region_factor = 1.0 + 0.2 * (regions.index(region) / len(regions))
            sales = int(base * seasonal_factor * region_factor)
            q_sales.append(sales)
        data[region][product] = q_sales

# -----------------------------
# 2. Aggregate to Heatmap Matrix (e.g., Region vs Product)
# -----------------------------
# We'll visualize total annual sales per region-product pair
matrix = []
for region in regions:
    row = []
    for product in products:
        total = sum(data[region][product])
        row.append(total)
    matrix.append(row)

# -----------------------------
# 3. Plot Heatmap
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 6))
cax = ax.imshow(matrix, cmap="YlOrRd")

# Set labels
ax.set_xticks(range(len(products)))
ax.set_xticklabels(products, rotation=45, ha="right", fontsize=10)
ax.set_yticks(range(len(regions)))
ax.set_yticklabels(regions, fontsize=10)
ax.set_title("Annual Sales Heatmap (Region vs Product)", fontsize=14, fontweight="bold")

# Add colorbar
cbar = fig.colorbar(cax, ax=ax)
cbar.set_label("Total Sales (USD)", rotation=270, labelpad=15)

# -----------------------------
# 4. Annotate Heatmap Values
# -----------------------------
for i, region in enumerate(regions):
    for j, product in enumerate(products):
        value = matrix[i][j]
        ax.text(j, i, f"${value/1000:.0f}k", ha="center", va="center", color="black", fontsize=9)

plt.tight_layout()
plt.show()
