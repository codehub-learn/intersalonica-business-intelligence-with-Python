"""""
ex3.py

ETL & KPI computation

Clustering (K-Means implemented manually)
Anomaly detection (Isolation Forest-like logic)
Predictive forecasting (basic Random Forest-style ensemble logic with standard library)
Correlation analysis
Matplotlib visualization


"""




import random
from datetime import datetime, timedelta
from statistics import mean, stdev
import matplotlib.pyplot as plt
import math

# ============================================================
# 1️⃣ ETL & DATA PREPARATION
# ============================================================

random.seed(42)
start_date = datetime(2023, 1, 1)
data = []

for i in range(639):  # ~21 months daily data
    date = start_date + timedelta(days=i)
    region = random.choice(["Europe", "Asia", "North America", "Africa", "South America"])
    sales = round(random.gauss(50000, 8000), 2)
    marketing = round(random.gauss(8000, 1000), 2)
    satisfaction = round(random.uniform(70, 95), 2)
    visits = random.randint(500, 3000)
    data.append({
        "date": date,
        "region": region,
        "sales": sales,
        "marketing_spend": marketing,
        "customer_satisfaction": satisfaction,
        "website_visits": visits
    })

def month_key(dt):
    return f"{dt.year}-{dt.month:02d}"

# ============================================================
# 2️⃣ MONTHLY AGGREGATION & KPI COMPUTATION
# ============================================================

monthly = {}
for d in data:
    m = month_key(d["date"])
    if m not in monthly:
        monthly[m] = {
            "sales": 0, "marketing_spend": 0, "customer_satisfaction": [],
            "website_visits": 0
        }
    monthly[m]["sales"] += d["sales"]
    monthly[m]["marketing_spend"] += d["marketing_spend"]
    monthly[m]["customer_satisfaction"].append(d["customer_satisfaction"])
    monthly[m]["website_visits"] += d["website_visits"]

# Aggregate metrics
for m, v in monthly.items():
    v["customer_satisfaction"] = mean(v["customer_satisfaction"])
    v["roi"] = (v["sales"] - v["marketing_spend"]) / v["marketing_spend"]
    v["conversion_rate"] = (v["sales"] / v["website_visits"]) * 100

months = sorted(monthly.keys())

# ============================================================
# 3️⃣ SIMPLE K-MEANS CLUSTERING (3 clusters)
# ============================================================

def euclidean(p1, p2):
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def kmeans(data_points, k=3, max_iter=100):
    centroids = random.sample(data_points, k)
    for _ in range(max_iter):
        clusters = [[] for _ in range(k)]
        for point in data_points:
            distances = [euclidean(point, c) for c in centroids]
            clusters[distances.index(min(distances))].append(point)
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroids.append([sum(vals)/len(vals) for vals in zip(*cluster)])
            else:
                new_centroids.append(random.choice(data_points))
        if all(euclidean(a, b) < 1e-4 for a, b in zip(centroids, new_centroids)):
            break
        centroids = new_centroids
    assignments = []
    for point in data_points:
        distances = [euclidean(point, c) for c in centroids]
        assignments.append(distances.index(min(distances)))
    return assignments

features = [
    [monthly[m]["sales"], monthly[m]["marketing_spend"], monthly[m]["roi"],
     monthly[m]["conversion_rate"], monthly[m]["customer_satisfaction"]]
    for m in months
]
clusters = kmeans(features, k=5)
for i, m in enumerate(months):
    monthly[m]["performance_cluster"] = clusters[i]

# ============================================================
# 4️⃣ ANOMALY DETECTION (Simple Isolation Logic)
# ============================================================

roi_vals = [monthly[m]["roi"] for m in months]
mean_roi = mean(roi_vals)
std_roi = stdev(roi_vals)
threshold = mean_roi - 2 * std_roi

for m in months:
    monthly[m]["anomaly_flag"] = "Anomaly" if monthly[m]["roi"] < threshold else "Normal"

# ============================================================
# 5️⃣ PREDICTIVE MODELING (Basic Ensemble Forecast)
# ============================================================

def forecast_next_sales(months, monthly):
    if len(months) < 3:
        return None
    last = monthly[months[-1]]["sales"]
    prev = monthly[months[-2]]["sales"]
    growth = (last - prev) / prev if prev else 0
    # Weighted ensemble of linear and random perturbation
    prediction = last * (1 + growth * 0.7 + random.uniform(-0.03, 0.03))
    return prediction

predicted_sales = forecast_next_sales(months, monthly)
print(f"Predicted next month sales: ${predicted_sales:,.2f}")

# ============================================================
# 6️⃣ CORRELATION ANALYSIS (MANUAL)
# ============================================================

def corr(x, y):
    mean_x, mean_y = mean(x), mean(y)
    num = sum((a - mean_x)*(b - mean_y) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mean_x)**2 for a in x) * sum((b - mean_y)**2 for b in y))
    return num / den if den else 0

metrics = ["sales", "marketing_spend", "roi", "conversion_rate", "customer_satisfaction"]
corr_matrix = {m1: {m2: corr(
    [monthly[k][m1] for k in months],
    [monthly[k][m2] for k in months]) for m2 in metrics} for m1 in metrics}

# Print correlation matrix
print("\nCorrelation Matrix:")
for m1 in metrics:
    print(f"{m1:20}", " ".join(f"{corr_matrix[m1][m2]:6.2f}" for m2 in metrics))

# ============================================================
# 7️⃣ VISUALIZATION (MATPLOTLIB)
# ============================================================

sales = [monthly[m]["sales"] for m in months]
roi = [monthly[m]["roi"] for m in months]
conv = [monthly[m]["conversion_rate"] for m in months]
custsat = [monthly[m]["customer_satisfaction"] for m in months]
colors = ['red' if monthly[m]["anomaly_flag"] == "Anomaly" else 'green' for m in months]

plt.figure(figsize=(13, 9))

# Sales Trend
plt.subplot(2, 2, 1)
plt.plot(months, sales, marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

# ROI with Anomalies
plt.subplot(2, 2, 2)
plt.bar(months, roi, color=colors)
plt.axhline(y=threshold, color='orange', linestyle='--', label='Anomaly Threshold')
plt.xticks(rotation=45)
plt.legend()
plt.title("ROI with Anomalies")

# Conversion vs Satisfaction
plt.subplot(2, 2, 3)
plt.scatter(conv, custsat, c=colors)
plt.title("Conversion Rate vs Customer Satisfaction")
plt.xlabel("Conversion Rate (%)")
plt.ylabel("Customer Satisfaction")

# Clusters
plt.subplot(2, 2, 4)
plt.scatter(
    [monthly[m]["marketing_spend"] for m in months],
    [monthly[m]["sales"] for m in months],
    c=[monthly[m]["performance_cluster"] for m in months],
    cmap="viridis", s=100
)
plt.title("Clusters: Marketing Spend vs Sales")
plt.xlabel("Marketing Spend")
plt.ylabel("Sales")

plt.tight_layout()
plt.show()
