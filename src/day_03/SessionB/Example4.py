"""
Preparation for ETL processes

- Reading data from files
- Data cleaning
- Data transformation
- Data aggregation


- OLTP 
Product (ProductId, Name, Price)
Customer (CustomerId, Name, Region)

Order(OrderId, CustomerId, OrderDate, DueDate, ShippingDate)
OrderItem(OrderItemId, OrderId, ProductId, Quantity, Discount, Tax, Freight, Tip)


- Star Schema for Data Warehouse
---------------------------
FactSale(OrderId, OrderItemId, ProductKey, CustomerKey, 
OrderDateKey, DueDateKey, ShippingDateKey
 Price, Quantity, Discount, Tax, Freight, Tip)

DimDate( DateKey, Calendar Information)

DimProduct(ProductKey, ProductId, Name,Price, StartDate, EndDate, IsCurrent )

DimCustomer(CustomerKey, CustomerId, Name, Region, StartDate, EndDate, IsCurrent )

----------------------
Questions
1. relating fact tables
2. very large fact tables


"""