import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(0)
df = pd.DataFrame(np.random.randn(200, 12), columns=[f"Feat_{i}" for i in range(12)])

corr = df.corr()

plt.figure(figsize=(14, 10))
sns.heatmap(
    corr, 
    annot=False, 
    cmap="coolwarm",
    linewidths=0.8,
    linecolor='black',
    square=True,
    cbar_kws={'shrink': 0.8}
)
plt.title("Advanced Correlation Heatmap")
plt.show()
