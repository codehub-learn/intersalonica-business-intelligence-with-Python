# radar plot demo for kpis
import random
import matplotlib.pyplot as plt
import numpy as np
random.seed(42)
# Sample data for 5 business branches and 5 KPIs
branches = [f"Branch {i+1}" for i in range(5)]
kpis = ["Revenue", "Marketing Spend", "Customer Satisfaction", "Operational Cost", "Employee Productivity"]
data = []
for _ in range(5):
    revenue = random.uniform(2000, 6000)
    marketing_spend = revenue * random.uniform(0.18, 0.25)
    customer_satisfaction = random.uniform(70, 95)
    operational_cost = revenue * random.uniform(0.5, 0.7)
    employee_productivity = random.uniform(60, 90)
    data.append([revenue, marketing_spend, customer_satisfaction, operational_cost, employee_productivity])

# Normalize data for radar plot
def normalize_column(values):   

    vmin, vmax = min(values), max(values)
    return [(v - vmin) / (vmax - vmin + 1e-6) for v in values]  
normalized_data = list(map(list, zip(*data)))  # transpose
normalized_data = [normalize_column(col) for col in normalized_data]
normalized_data = list(zip(*normalized_data))  # transpose back
# Radar plot setup
num_vars = len(kpis)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Complete the loop
angles += angles[:1]
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
for i, entity in enumerate(normalized_data):
    values = entity + entity[:1]
    ax.plot(angles, values, marker='o', linewidth=1.5, label=branches[i])
    ax.fill(angles, values, alpha=0.25)
# Customize the radar plot
ax.set_xticks(angles[:-1])
ax.set_xticklabels(kpis, fontsize=12)
ax.set_yticklabels([])
plt.title("Radar Plot — Business Branch KPI Comparison", fontsize=14, weight="bold", y=1.1)
plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.show()

