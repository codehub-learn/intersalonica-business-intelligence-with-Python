"""
ex8.py
Create a Bubble Chart Matrix for synthetic business intelligence data.

Bubble Chart Matrix

Use case: Correlate three metrics in one plot.
X = Revenue
Y = Marketing Spend
Bubble size = Customer Satisfaction
Bubble color = Operational Cost
👉 Great for multi-variable storytelling in BI dashboards.
"""

import random
import matplotlib.pyplot as plt

# Step 1: Generate synthetic business data
n = 50
revenue = [random.uniform(1000, 5000) for _ in range(n)]
marketing_spend = [r * random.uniform(0.18, 0.25) + random.uniform(-200, 200) for r in revenue]
customer_satisfaction = [70 + (r/1000)*2 - (m/600)*0.8 + random.uniform(-5, 5) for r, m in zip(revenue, marketing_spend)]
operational_cost = [r * random.uniform(0.5, 0.7) + random.uniform(-100, 100) for r in revenue]

# Step 2: Normalize values for bubble size and color mapping
min_cost = min(operational_cost)
max_cost = max(operational_cost)
min_satisfaction = min(customer_satisfaction)
max_satisfaction = max(customer_satisfaction)

def normalize(value, vmin, vmax):
    return (value - vmin) / (vmax - vmin + 1e-6)

bubble_sizes = [300 * normalize(cs, min_satisfaction, max_satisfaction) + 50 for cs in customer_satisfaction]
colors = [normalize(c, min_cost, max_cost) for c in operational_cost]

# Step 3: Create Bubble Chart
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    revenue,
    marketing_spend,
    s=bubble_sizes,
    c=colors,
    cmap='coolwarm',
    alpha=0.7,
    edgecolors='black'
)

plt.title("Business KPI Bubble Chart Matrix", fontsize=14, weight="bold")
plt.xlabel("Revenue", fontsize=12)
plt.ylabel("Marketing Spend", fontsize=12)
plt.colorbar(scatter, label="Operational Cost")

# Step 4: Add annotations for high-revenue points
for i in range(n):
    if revenue[i] > 4800:  # label only top performers
        plt.text(revenue[i], marketing_spend[i], f"{customer_satisfaction[i]:.1f}%", fontsize=8,
                 ha="center", va="center", color="black", weight="bold")

plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()
