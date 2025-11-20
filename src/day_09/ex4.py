"""
Customer Segmentation (K-Means Clustering)

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

np.random.seed(0)

df = pd.DataFrame({
    "Annual_Spend": np.random.normal(50000, 12000, 300),
    "Visit_Frequency": np.random.normal(20, 5, 300)
})

kmeans = KMeans(n_clusters=4, random_state=0).fit(df)
df["Cluster"] = kmeans.labels_

plt.figure(figsize=(10, 8))
for c in df["Cluster"].unique():
    cluster = df[df["Cluster"] == c]
    plt.scatter(cluster["Annual_Spend"], cluster["Visit_Frequency"], label=f"Cluster {c}")

plt.xlabel("Annual Spend (€)")
plt.ylabel("Visits per Year")
plt.title("Customer Segmentation using K-Means")
plt.legend()
plt.grid(True)
plt.show()
