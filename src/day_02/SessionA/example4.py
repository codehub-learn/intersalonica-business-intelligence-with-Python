import day_02.SessionA.example3 as salesanalytics

if __name__ == "__main__":
    data = [
        {"Product": "Laptop", "Revenue": 1200, "Cost": 800},
        {"Product": "Tablet", "Revenue": 500, "Cost": 300},
        {"Product": "Smartphone", "Revenue": 800, "Cost": 600},
    ]

    analytics = salesanalytics.SalesAnalytics(data)

    revenue = analytics.total_revenue
    print(revenue)

    print("Total Revenue:", analytics.total_revenue())
    print("Total Profit:", analytics.total_profit())
    print("Average Revenue:", analytics.average_revenue())
    print("Best Product:", analytics.best_product())
    print("Profit Margins:", analytics.profit_margins())  
    print("Low Margin Products (<30%):", analytics.low_margin_products(30))