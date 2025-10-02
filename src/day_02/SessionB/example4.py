import pyodbc

# -------------------------------
# 1️⃣ Connect to Northwind DB
# -------------------------------
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost;'          # Replace with your server
    'DATABASE=Northwind;'        # Northwind database
    'UID=sa;'                    # SQL login
    'PWD=passw0rd;'          # SQL password
    'TrustServerCertificate=yes;'
    'Encrypt=yes;'
)
cursor = conn.cursor()

# -------------------------------
# 2️⃣ Fetch Sales Data
# -------------------------------
cursor.execute("""
    SELECT od.ProductID, p.ProductName, od.UnitPrice, od.Quantity
    FROM [Order Details] od
    JOIN Products p ON od.ProductID = p.ProductID
""")

sales_list = []
for row in cursor.fetchall():
    sales_list.append({
        "Product": row.ProductName,
        "Revenue": row.UnitPrice * row.Quantity,     # Revenue
        "Cost": float(row.UnitPrice) * row.Quantity * 0.6  # Assume 60% cost
    })

cursor.close()
conn.close()

# -------------------------------
# 3️⃣ BI Analysis Class
# -------------------------------
class SalesAnalytics:
    """BI analytics for Northwind sales."""

    def __init__(self, sales_data):
        self.sales_data = sales_data

    def total_revenue(self):
        return sum(float(item["Revenue"]) for item in self.sales_data)

    def total_profit(self):
        return sum(float(item["Revenue"]) - item["Cost"] for item in self.sales_data)

    def best_product(self):
        return max(self.sales_data, key=lambda x: float(x["Revenue"]))["Product"]

    def profit_margins(self):
        return {
            item["Product"]: round((float(item["Revenue"])  - item["Cost"]) / float(item["Revenue"])  * 100, 2)
            for item in self.sales_data
        }

    def low_margin_products(self, threshold=20):
        margins = self.profit_margins()
        return [product for product, margin in margins.items() if margin < threshold]

# -------------------------------
# 4️⃣ Run BI Analysis
# -------------------------------
analytics = SalesAnalytics(sales_list)

print("Total Revenue:", analytics.total_revenue())
print("Total Profit:", analytics.total_profit())
print("Best Product by Revenue:", analytics.best_product())
print("Profit Margins (%):", analytics.profit_margins())
print("Low Margin Products (<50%):", analytics.low_margin_products(50))
