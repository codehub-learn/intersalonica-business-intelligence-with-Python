class SalesAnalytics:
    """A simple Business Intelligence class for sales analysis without pandas."""

    def __init__(self, sales_data: list[dict]):
        """
        Args:
            sales_data (list of dict): Each dict must contain 
                                       'Product', 'Revenue', and 'Cost'.
        """
        self.sales_data = sales_data

    def total_revenue(self)-> float:
        return sum(item["Revenue"] for item in self.sales_data)

    def total_profit(self)-> float:
        return sum(item["Revenue"] - item["Cost"] for item in self.sales_data)

    def average_revenue(self)-> float:
        return round(self.total_revenue() / len(self.sales_data), 2)

    def best_product(self)-> str:
        return max(self.sales_data, key=lambda x: x["Revenue"])  ["Product"]

    def profit_margins(self)-> dict:
        """Return dictionary of products and their profit margins %."""
        return {
            item["Product"]: round((item["Revenue"] - item["Cost"]) / item["Revenue"] * 100, 2)
            for item in self.sales_data
        }

    def low_margin_products(self, threshold:float=20)-> list:
        """
        Identify products with profit margin below the given threshold.

        Args:
            threshold (float): Margin percentage below which product is considered low-margin.

        Returns:
            list: Names of products with low profit margin.
        """
        margins = self.profit_margins()
        return [product for product, margin in margins.items() if margin < threshold]





if __name__ == "__main__":
    data = [
        {"Product": "Laptop", "Revenue": 1200, "Cost": 800},
        {"Product": "Tablet", "Revenue": 350, "Cost": 300},
        {"Product": "Smartphone", "Revenue": 800, "Cost": 600},
        {"Product": "Tablet", "Revenue": 360, "Cost": 300},
        {"Product": "Smartphone", "Revenue": 800, "Cost": 600,"cate":"xx"},
    ]

    analytics = SalesAnalytics(data)

    print("Total Revenue:", analytics.total_revenue())
    print("Total Profit:", analytics.total_profit())
    print("Average Revenue:", analytics.average_revenue())
    print("Best Product:", analytics.best_product())
    print("Profit Margins:", analytics.profit_margins())  
    print("Low Margin Products (<30%):", analytics.low_margin_products(30))  

