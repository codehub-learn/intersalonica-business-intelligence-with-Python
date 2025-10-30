"""
ex10.py
Create a Parallel Coordinates Plot

Use case: Compare multiple variables for each entity (e.g., regions, customers).
Each line represents one entity across several metrics.
👉 Ideal for multi-dimensional comparisons
        
        .
"""

import random
import plotly.express as px

# Step 1: Generate synthetic business data for multiple branches
n_entities = 12
branches = [f"Branch {i+1}" for i in range(n_entities)]

data = []
for _ in range(n_entities):
    revenue = random.uniform(2000, 6000)
    marketing_spend = revenue * random.uniform(0.18, 0.25)
    customer_satisfaction = random.uniform(70, 95)
    operational_cost = revenue * random.uniform(0.5, 0.7)
    employee_productivity = random.uniform(60, 90)
    data.append({
        "Branch": branches[_],
        "Revenue": revenue,
        "Marketing Spend": marketing_spend,
        "Customer Satisfaction": customer_satisfaction,
        "Operational Cost": operational_cost,
        "Employee Productivity": employee_productivity
    })

# Step 2: Create Parallel Coordinates Plot
fig = px.parallel_coordinates(
    data,
    dimensions=["Revenue", "Marketing Spend", "Customer Satisfaction", "Operational Cost", "Employee Productivity"],
    color="Revenue",                     # Color lines by Revenue
    color_continuous_scale=px.colors.sequential.Viridis,
    labels={
        "Revenue": "Revenue ($)",
        "Marketing Spend": "Marketing Spend ($)",
        "Customer Satisfaction": "Satisfaction (%)",
        "Operational Cost": "Operational Cost ($)",
        "Employee Productivity": "Productivity Score"
    },
    title="Interactive Parallel Coordinates Plot — Branch KPI Comparison"
)

# Step 3: Show interactive plot
fig.show()
