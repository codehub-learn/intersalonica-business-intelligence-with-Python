--changes in OLTP
USE [Northwind]
GO


select * from [dbo].[Customers]

-- update
update [dbo].[Customers] set 
	Address = 'Athens'
	, City ='Athens'
	, [Region] = 'Athens'       
	,[PostalCode]='11526'
    ,[Country]  ='Greece'  
where [CustomerID] ='ALFKI';

-- insert
INSERT INTO [dbo].[Customers]
           ([CustomerID]	,[CompanyName]
           ,[ContactName]	,[ContactTitle]
           ,[Address]       ,[City]
           ,[Region]        ,[PostalCode]
           ,[Country]       ,[Phone]        ,[Fax])
     VALUES
           ('GATI', 'Gati Company'
           ,'Dimitris', 'Mr.'
           ,'Athens','Athens','Athens'
           ,11526
           ,'Greece', 'xxxx', 'fax' );

-- find a  customer with no orders to delete
select c.CustomerID 
	from customers c left join [Orders] od
	on od.CustomerID = c.CustomerID
where od.OrderID is null;
		   
 
-- delete
delete from [dbo].[Customers] where [CustomerID] = 'PARIS';


--- insert new facts
INSERT INTO [dbo].[Orders]
           ([CustomerID] ,[EmployeeID] ,[OrderDate] )
     VALUES
           ('ALFKI'  ,2 ,'1998-05-07' )


declare  @InsertedOrderId int =@@IDENTITY;

INSERT INTO [dbo].[Order Details]
        ([OrderID]   ,[ProductID]
        ,[UnitPrice]  ,[Quantity]
        ,[Discount])
VALUES
        (@InsertedOrderId, 5, 22.3, 3, 0),
		(@InsertedOrderId, 6, 18.4, 2, 0),
		(@InsertedOrderId, 7, 22.5, 6, 0.5);
 
          
 

