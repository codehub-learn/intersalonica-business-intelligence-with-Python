"""
Advanced Profitability Heatmap (Products × Regions)
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

products = [f"P{i}" for i in range(1, 11)]
regions = ["EU", "US", "APAC", "MEA"]

data = np.random.uniform(-0.2, 0.35, (10, 4))  # profit margin

df = pd.DataFrame(data, index=products, columns=regions)

plt.figure(figsize=(12, 8))
sns.heatmap(df, annot=True, fmt=".2%", cmap="RdYlGn", center=0)
plt.title("Profit Margin Heatmap (Products × Regions)")
plt.show()
