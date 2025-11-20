"""

Financial Risk Dashboard (Value at Risk + Distribution)
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(1)

# simulated portfolio returns
returns = np.random.normal(0.001, 0.02, 1000)

VaR_95 = np.percentile(returns, 5)

plt.figure(figsize=(12, 6))
sns.histplot(returns, kde=True, bins=40)

plt.axvline(VaR_95, color="red", linewidth=2)
plt.text(VaR_95, 40, f"VaR 95% = {VaR_95:.4f}", color="red")

plt.title("Portfolio Return Distribution + Value at Risk")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.show()
