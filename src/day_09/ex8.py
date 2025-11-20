"""
Supply Chain — Inventory Levels + Demand Oscillations
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

days = np.arange(1, 200)
demand = 50 + 30*np.sin(days/8) + np.random.normal(0, 5, len(days))
inventory = 300 - np.cumsum(demand - 45)

plt.figure(figsize=(14, 6))
plt.plot(days, demand, label="Demand", linewidth=2)
plt.plot(days, inventory, label="Inventory Level", linewidth=3)
plt.axhline(50, color='red', linestyle='--', label="Reorder Point")

plt.title("Supply Chain: Demand vs Inventory Level")
plt.xlabel("Day")
plt.ylabel("Units")
plt.legend()
plt.grid(True)
plt.show()
