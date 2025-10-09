import xml.etree.ElementTree as ET

class XMLSalesAnalytics:
    """Business Intelligence class to analyze sales data from XML."""

    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.sales_data = self.load_xml()

    def load_xml(self)-> list:
        """Parse XML and return list of sales dictionaries."""
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        sales = []
        for sale in root.findall('Sale'):
            sales.append({
                "Product": sale.find('Product').text,
                "Revenue": float(sale.find('Revenue').text),
                "Cost": float(sale.find('Cost').text)
            })
        return sales

    def total_revenue(self):
        return sum(item["Revenue"] for item in self.sales_data)

    def total_profit(self):
        return sum(item["Revenue"] - item["Cost"] for item in self.sales_data)

    def best_product(self):
        return max(self.sales_data, key=lambda x: x["Revenue"])["Product"]

    def profit_margins(self):
        return {
            item["Product"]: round((item["Revenue"] - item["Cost"]) / item["Revenue"] * 100, 2)
            for item in self.sales_data
        }

    def low_margin_products(self, threshold=20):
        margins = self.profit_margins()
        return [product for product, margin in margins.items() if margin < threshold]


if __name__ == "__main__":
    analytics = XMLSalesAnalytics("data/sales.xml")

    print("Total Revenue:", analytics.total_revenue())
    print("Total Profit:", analytics.total_profit())
    print("Best Product by Revenue:", analytics.best_product())
    print("Profit Margins (%):", analytics.profit_margins())
    print("Low Margin Products (<20%):", analytics.low_margin_products())
