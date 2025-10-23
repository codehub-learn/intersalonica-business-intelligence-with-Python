-- 1. creates staging database


use master
go
--create db

USE master
GO
if exists (select * from sysdatabases where name='NorthWindStaging')
begin
	ALTER DATABASE NorthWindStaging 
	SET SINGLE_USER 
	WITH ROLLBACK IMMEDIATE;
		drop database NorthWindStaging

end
go



create database [NorthWindStaging]
GO


--create & load table [Employees] in staging
use NorthWindStaging


select 
	EmployeeID,
	FirstName,
	LastName,
	Title
	into [Employees]
from [Northwind].[dbo].[Employees];


select 
	CustomerID,  CompanyName,  ContactName, ContactTitle, Address, 
	City, Region, PostalCode, Country
	into Customers
from  [Northwind].[dbo].Customers;


select 
	ProductID,  ProductName,  Discontinued, companyname, categoryname
	into Products
from [Northwind].[dbo].Products p
	inner join [Northwind].[dbo].[Suppliers] s
	on p.[SupplierID]=s.[SupplierID]
	inner join [Northwind].[dbo].[Categories] c
	on p.[CategoryID]=c.[CategoryID];

 
select
	ProductID,  o.OrderId,  EmployeeId,  CustomerId,  OrderDate,  ShippedDate, unitprice,  quantity,
	discount
	into sales
from [Northwind].[dbo].Orders o
	inner join [Northwind].[dbo].[Order Details]  d on o.OrderID= d.OrderId;
	

 select min(orderdate), max(shippeddate) from sales;