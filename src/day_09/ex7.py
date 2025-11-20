"""
HR Analytics — Employee Attrition Probability

"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(0)

df = pd.DataFrame({
    "Age": np.random.randint(22, 60, 500),
    "Satisfaction": np.random.uniform(0, 1, 500),
    "Attrition_Prob": np.random.beta(2, 5, 500)
})

plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=df,
    x="Age",
    y="Satisfaction",
    hue="Attrition_Prob",
    palette="coolwarm",
    size="Attrition_Prob",
    sizes=(20, 200)
)

plt.title("HR Attrition Probability by Age & Satisfaction")
plt.show()

