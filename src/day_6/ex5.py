"""
ex5.py
Create a correlation matrix heatmap for synthetic business intelligence data.
The dataset includes:
- Revenue
- Marketing Spend
- Customer Satisfaction
- Operational Cost
- Employee Productivity
The correlations to highlight:
    

Revenue ↔ Marketing Spend → strong positive correlation
Revenue ↔ Operational Cost → strong positive correlation
Revenue ↔ Customer Satisfaction → mild positive
Operational Cost ↔ Employee Productivity → slight negative
"""

import random
import math
import matplotlib.pyplot as plt

# Step 1: Generate synthetic business data
n = 50
revenue = [random.uniform(1000, 5000) for _ in range(n)]
marketing_spend = [r * random.uniform(0.15, 0.25) + random.uniform(-200, 200) for r in revenue]
customer_satisfaction = [80 + (r/1000) * 2 - (m/500) * 0.5 + random.uniform(-3, 3) for r, m in zip(revenue, marketing_spend)]
operational_cost = [r * random.uniform(0.5, 0.7) + random.uniform(-150, 150) for r in revenue]
employee_productivity = [70 + (r/5000) * 20 - (c/4000) * 10 + random.uniform(-5, 5) for r, c in zip(revenue, operational_cost)]

data = {
    "Revenue": revenue,
    "Marketing Spend": marketing_spend,
    "Customer Satisfaction": customer_satisfaction,
    "Operational Cost": operational_cost,
    "Employee Productivity": employee_productivity
}

# Step 2: Compute correlation manually
def correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    num = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
    den_x = math.sqrt(sum((a - mean_x)**2 for a in x))
    den_y = math.sqrt(sum((b - mean_y)**2 for b in y))
    return num / (den_x * den_y)

keys = list(data.keys())
size = len(keys)
corr_matrix = [[correlation(data[keys[i]], data[keys[j]]) for j in range(size)] for i in range(size)]

# Step 3: Visualization - Correlation Matrix Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)

# Step 4: Customize visualization
ax.set_xticks(range(size))
ax.set_yticks(range(size))
ax.set_xticklabels(keys, rotation=45, ha="right")
ax.set_yticklabels(keys)
plt.colorbar(im, ax=ax, label="Correlation Coefficient")

# Step 5: Annotate values
for i in range(size):
    for j in range(size):
        ax.text(j, i, f"{corr_matrix[i][j]:.2f}", ha="center", va="center", color="black")

plt.title("Business Intelligence Correlation Matrix")
plt.tight_layout()
plt.show()
