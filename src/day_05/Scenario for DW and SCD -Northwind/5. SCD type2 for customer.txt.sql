-- OLTP -> staging

USE [NorthWindStaging]
GO

truncate table [NorthWindStaging].[dbo].[Customers];

insert into Customers(CustomerID,  CompanyName,  ContactName, ContactTitle, Address, 
	City, Region, PostalCode, Country)
select 
	CustomerID,  CompanyName,  ContactName, ContactTitle, Address, 
	City, Region, PostalCode, Country
from  [Northwind].[dbo].Customers;

-----------------------------------------------------------
truncate table [NorthWindStaging].[dbo].Sales;

insert into sales
(ProductID,  o.OrderId,  EmployeeId,  CustomerId,  OrderDate,  ShippedDate, unitprice,  quantity,
	discount)
select
	ProductID,  o.OrderId,  EmployeeId,  CustomerId,  OrderDate,  ShippedDate, unitprice,  quantity,
	discount
from [Northwind].[dbo].Orders o
	inner join [Northwind].[dbo].[Order Details]  d on o.OrderID= d.OrderId
where OrderDate>='1998-05-07';

 

 select * from [NorthWindStaging].[dbo].Sales;
--- staging ->DW
 
drop table if exists [NorthWindStaging].[dbo].Staging_DimCustomer;

create table [NorthWindStaging].[dbo].Staging_DimCustomer (
	CustomerKey INT IDENTITY(1,1) NOT NULL,
	CustomerID VARCHAR(5) NOT NULL,
	CompanyName VARCHAR(40) NOT NULL,
	ContactName VARCHAR(40) NOT NULL,
	ContactTitle VARCHAR(30) NOT NULL,
	CustomerCountry VARCHAR(15) NOT NULL,
	CustomerRegion VARCHAR(15) DEFAULT 'N/A' NOT NULL,
	CustomerCity VARCHAR(15) NOT NULL,
	CustomerPostalCode VARCHAR(10) NOT NULL,
	RowIsCurrent INT DEFAULT 1 NOT NULL,
	RowStartDate DATE DEFAULT '1899-12-31' NOT NULL,
	RowEndDate DATE DEFAULT '9999-12-31' NOT NULL,
	RowChangeReason VARCHAR(200) NULL
);

------------------------------
Insert into [NorthWindStaging].[dbo].Staging_DimCustomer(
	CustomerID, CompanyName, ContactName,
	ContactTitle, CustomerCountry, CustomerRegion,
	CustomerCity, CustomerPostalCode)
	(  Select [CustomerID]customer_id, [CompanyName], [ContactName], [ContactTitle], [country],
        case when [region] is null then 'n/a' else [region] end,
        city,
        case when [PostalCode] is null then 'n/a' else [PostalCode] end
from [NorthWindStaging].[dbo].[customers]  );

 -------------------------------------------------


--drop the constraints 



alter table [NorthwindDW].[dbo].factsales
	drop constraint factsales_dimcustomer_customerkey_fk;

alter table [NorthwindDW].[dbo].factsales
	drop constraint factsales_dimemployee_employeekey_fk;	

alter table [NorthwindDW].[dbo].factsales
	drop constraint factsales_dimproduct_productkey_fk;

alter table [NorthwindDW].[dbo].factsales
	drop constraint factsales_dimdate_date_dim_id_fk;

alter table [NorthwindDW].[dbo].factsales
	drop constraint factsales_dimdate_date_dim_id_fk_2;		





 -------------------------------------------------





INSERT INTO [NorthwindDW].[dbo].DimCustomer (
	CustomerID, CompanyName, ContactName,
	ContactTitle, CustomerCountry, CustomerRegion,
	CustomerCity, CustomerPostalCode
	 , RowStartDate, RowChangeReason )
SELECT 
	CustomerID, CompanyName, ContactName,
	ContactTitle, CustomerCountry, CustomerRegion,
	CustomerCity, CustomerPostalCode
	   ,CAST(GetDate() AS Date)	  ,ActionName
FROM
(
	MERGE [NorthwindDW].[dbo].DimCustomer AS target
		USING [NorthWindStaging].[dbo].Staging_DimCustomer as source
		ON target.[CustomerID] = source.[CustomerID]
	 WHEN MATCHED 	 AND 
	 source.CustomerCity <> target.CustomerCity  
	 AND target.[RowIsCurrent] = 1 
	 THEN UPDATE SET
		 target.RowIsCurrent = 0,
		 target.RowEndDate = dateadd(day, -1, CAST(GetDate() AS Date)) ,
		 target.RowChangeReason = 'UPDATED NOT CURRENT'
	 WHEN NOT MATCHED THEN
	   INSERT  (
			CustomerID, CompanyName, ContactName,
			ContactTitle, CustomerCountry, CustomerRegion,
			CustomerCity, CustomerPostalCode
		   ,  RowStartDate,   RowChangeReason
	   )
	   VALUES( 
		   source.CustomerID,source. CompanyName,source.  ContactName,
			source. ContactTitle, source. CustomerCountry, source. CustomerRegion,
			source. CustomerCity, source. CustomerPostalCode
		   ,CAST(GetDate() AS Date),
		   'NEW RECORD'
	   )
	WHEN NOT MATCHED BY Source THEN
		UPDATE SET 
			Target.RowEndDate= dateadd(day, -1, CAST(GetDate() AS Date))
			,target.RowIsCurrent = 0
			,Target.RowChangeReason  = 'SOFT DELETE'
	OUTPUT 
		 source.CustomerID,source. CompanyName,source.  ContactName,
			source. ContactTitle, source. CustomerCountry, source. CustomerRegion,
			source. CustomerCity, source. CustomerPostalCode
		,$Action as ActionName   
) AS Mrg
WHERE Mrg.ActionName='UPDATE'
AND [CustomerID] IS NOT NULL;


------------------------------------------------
-- insert new facts ...


INSERT INTO [NorthwindDW].[dbo].FactSales(
    ProductKey, CustomerKey, EmployeeKey, OrderDateKey, ShippedDateKey,
    OrderID, Quantity, ExtendedPriceAmount, DiscountAmount, SoldAmount)
SELECT ProductKey, CustomerKey, EmployeeKey,
    CAST(FORMAT(OrderDate,'yyyyMMdd') AS INT),
    CAST(FORMAT(ShippedDate,'yyyyMMdd') AS INT),
    OrderID, Quantity, [UnitPrice]*[Quantity], [UnitPrice]*Discount, ([UnitPrice]*(1 - [Discount]))*[Quantity]
FROM 
    NorthwindStaging.dbo.Sales AS s
INNER JOIN NorthwindDW.dbo.DimCustomer AS c
    ON c.CustomerID=s.CustomerId
INNER JOIN NorthwindDW.dbo.DimEmployee AS e
    ON e.EmployeeID=s.EmployeeId
INNER JOIN NorthwindDW.dbo.DimProduct AS p
    ON p.ProductID=s.ProductID
