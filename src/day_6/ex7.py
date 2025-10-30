"""
ex7.py
Create a Parallel Coordinates Plot

Use case: Compare multiple variables for each entity (e.g., regions, customers).
Each line represents one entity across several metrics.
👉 Ideal for multi-dimensional comparisons.

"""

import random
import matplotlib.pyplot as plt

# Step 1: Generate synthetic business data for multiple branches
n_entities = 12  # number of business branches
branches = [f"Branch {i+1}" for i in range(n_entities)]

# Each branch has 5 KPIs
data = []
for _ in range(n_entities):
    revenue = random.uniform(2000, 6000)
    marketing_spend = revenue * random.uniform(0.18, 0.25)
    customer_satisfaction = random.uniform(70, 95)
    operational_cost = revenue * random.uniform(0.5, 0.7)
    employee_productivity = random.uniform(60, 90)
    data.append([revenue, marketing_spend, customer_satisfaction, operational_cost, employee_productivity])

metrics = ["Revenue", "Marketing Spend", "Customer Satisfaction", "Operational Cost", "Employee Productivity"]

# Step 2: Normalize each metric for fair comparison
def normalize_column(values):
    vmin, vmax = min(values), max(values)
    return [(v - vmin) / (vmax - vmin + 1e-6) for v in values]

normalized_data = list(map(list, zip(*data)))  # transpose
normalized_data = [normalize_column(col) for col in normalized_data]
normalized_data = list(zip(*normalized_data))  # transpose back

# Step 3: Draw Parallel Coordinates Plot
plt.figure(figsize=(10, 6))
x_positions = list(range(len(metrics)))

for i, entity in enumerate(normalized_data):
    plt.plot(x_positions, entity, marker='o', alpha=0.7, linewidth=1.5, label=branches[i])

# Step 4: Customize visualization
plt.xticks(x_positions, metrics, rotation=30, ha='right')
plt.title("Parallel Coordinates Plot — Business Branch Performance", fontsize=14, weight="bold")
plt.ylabel("Normalized KPI Value (0–1)")
plt.grid(True, linestyle="--", alpha=0.4)

# Optional: highlight a top performer
top_index = max(range(n_entities), key=lambda i: data[i][0])  # highest revenue
plt.plot(x_positions, normalized_data[top_index], color="red", linewidth=2.5, label=f"{branches[top_index]} (Top Revenue)")

plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.show()
