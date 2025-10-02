class SalesRecord:
    def __init__(self, product, revenue, cost):
        self.product = product
        self.revenue = revenue
        self.cost = cost

    def profit(self):
        return self.revenue - self.cost

    def margin(self):
        return round((self.profit() / self.revenue) * 100, 2)


if __name__ == "__main__":
    # Create objects
    record1 = SalesRecord("Laptop", 1200, 800)
    record2 = SalesRecord("Tablet", 500, 300)

    print(record1.product, "Profit:", record1.profit(), "Margin:", record1.margin())
    print(record2.product, "Profit:", record2.profit(), "Margin:", record2.margin())
