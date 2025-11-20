"""
Advanced Sales Forecast + Confidence Intervals
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Mock monthly sales
np.random.seed(42)
months = np.arange(1, 36)
sales = 20000 + months*500 + np.random.normal(0, 2000, len(months))

df = pd.DataFrame({"month": months, "sales": sales})

# train model
X = df[["month"]]
y = df["sales"]
model = LinearRegression().fit(X, y)

# future 12-month forecast
future_months = np.arange(36, 48).reshape(-1, 1)
forecast = model.predict(future_months)

# confidence interval
std = np.std(y - model.predict(X))
upper = forecast + 1.96 * std
lower = forecast - 1.96 * std

plt.figure(figsize=(14, 6))
plt.plot(df["month"], df["sales"], label="Actual Sales")
plt.plot(future_months, forecast, label="Forecast", linewidth=3)
plt.fill_between(future_months.flatten(), lower, upper, alpha=0.2, label="95% Confidence")
plt.title("Sales Forecast with Confidence Intervals")
plt.xlabel("Month")
plt.ylabel("Revenue (€)")
plt.legend()
plt.grid(True)
plt.show()
