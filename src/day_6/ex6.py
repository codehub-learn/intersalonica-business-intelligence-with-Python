"""
ex6.py
Create a scatterplot matrix for synthetic business intelligence data.   
The dataset includes:
- Revenue
- Marketing Spend
- Customer Satisfaction
- Operational Cost
- Employee Productivity
The insights to explore:

Scatterplot Matrix of Business KPIs

How Marketing Spend relates to Revenue (directly proportional)
Whether Operational Cost impacts Employee Productivity
Patterns like clusters or outliers

"""

import random
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

# Step 2: Create scatterplot matrix
keys = list(data.keys())
size = len(keys)
fig, axes = plt.subplots(size, size, figsize=(10, 10))
plt.subplots_adjust(wspace=0.4, hspace=0.4)

for i in range(size):
    for j in range(size):
        ax = axes[i][j]
        if i == j:
            # Plot histogram on diagonal
            ax.hist(data[keys[i]], bins=10, color="skyblue", edgecolor="black")
        else:
            # Scatter plots off-diagonal
            ax.scatter(data[keys[j]], data[keys[i]], alpha=0.7, color="teal")
        if i == size - 1:
            ax.set_xlabel(keys[j], rotation=45, fontsize=8)
        else:
            ax.set_xticklabels([])
        if j == 0:
            ax.set_ylabel(keys[i], fontsize=8)
        else:
            ax.set_yticklabels([])

plt.suptitle("Scatterplot Matrix of Business KPIs", fontsize=14)
plt.show()
