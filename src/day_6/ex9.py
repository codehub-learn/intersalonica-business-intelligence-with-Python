"""
ex9.py
Create a Network Correlation Graph with correlation coefficients for synthetic business intelligence data.
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
n = 60
revenue = [random.uniform(1000, 5000) for _ in range(n)]
marketing_spend = [r * random.uniform(0.18, 0.25) + random.uniform(-200, 200) for r in revenue]
customer_satisfaction = [75 + (r/1000)*1.5 - (m/500)*0.6 + random.uniform(-4, 4) for r, m in zip(revenue, marketing_spend)]
operational_cost = [r * random.uniform(0.55, 0.65) + random.uniform(-100, 100) for r in revenue]
employee_productivity = [70 + (r/5000)*20 - (c/4000)*12 + random.uniform(-5, 5) for r, c in zip(revenue, operational_cost)]

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

# Step 3: Layout nodes in a circle
radius = 3
positions = []
for i in range(size):
    angle = 2 * math.pi * i / size
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    positions.append((x, y))

# Step 4: Draw network graph with edge labels
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-4, 4)
ax.set_ylim(-4, 4)
ax.axis("off")

# Draw edges
for i in range(size):
    for j in range(i + 1, size):
        corr = corr_matrix[i][j]
        if abs(corr) > 0.2:  # Only show significant correlations
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            color = "red" if corr > 0 else "blue"
            linewidth = abs(corr) * 5
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, alpha=0.7)

            # Label correlation value at midpoint of edge
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y, f"{corr:+.2f}", fontsize=8, ha="center", va="center", color=color, fontweight="bold")

# Draw nodes
for i, (x, y) in enumerate(positions):
    ax.scatter(x, y, s=900, color="lightgray", edgecolor="black", zorder=3)
    ax.text(x, y, keys[i], ha="center", va="center", fontsize=10, weight="bold", zorder=4)

plt.title("Network Correlation Graph with Correlation Coefficients", fontsize=14, weight="bold")
plt.show()
