use master
go

-- 3. inserts data into the dw


Insert into [NorthwindDW].[dbo].[DimEmployee]([EmployeeID], [EmployeeName], [EmployeeTitle])
(Select [EmployeeID], concat([FirstName],[LastName]), [Title]
from [NorthWindStaging].[dbo].[Employees]);

 


 
Insert into [NorthwindDW].[dbo].dimcustomer (customerid, companyname, contactname, contacttitle, customercountry, customerregion, customercity, customerpostalcode)
(  Select [CustomerID]customer_id, [CompanyName], [ContactName], [ContactTitle], [country],
        case when [region] is null then 'n/a' else [region] end,
        city,
        case when [PostalCode] is null then 'n/a' else [PostalCode] end
from [NorthWindStaging].[dbo].[customers]  );




Insert into [NorthwindDW].[dbo].dimproduct (productid, productname, discontinued, suppliername, categoryname)
(Select [ProductID], [ProductName],
        case when discontinued = 0 then 'N' else 'Y' end,
        [CompanyName],
        [CategoryName]
from [NorthWindStaging].[dbo].[products]);



alter table [NorthwindDW].[dbo].factsales alter column shippeddatekey int null;

insert into [NorthwindDW].[dbo].factsales(productkey, customerkey, employeekey, orderdatekey, shippeddatekey, orderid, quantity, extendedpriceamount, discountamount, soldamount)
(select
p.productkey, c.customerkey, e.employeekey,
       dorder.[DateKey] as orderdatekey,
       dshipped.[DateKey] as shippeddatekey,
       s.orderid, s.quantity,
       s.quantity * s.[UnitPrice] as extendedpriceamount,
       s.quantity * s.[UnitPrice] * s.discount as discountedamount,
       s.quantity * s.[UnitPrice] * (1-s.discount) as soldamount
from [NorthWindStaging].[dbo].sales s
join [NorthwindDW].[dbo].dimcustomer c
on s.[CustomerID] = c.customerid
join [NorthwindDW].[dbo].dimemployee e
on s.employeeid = e.employeeid
join [NorthwindDW].[dbo].dimproduct p
on s.productid = p.productid
join  [NorthwindDW].[dbo].[DimDate] dorder --[dbo].dimdate
on s.[OrderDate] = dorder.[Date]   --date_actual
left join [NorthwindDW].[dbo].dimdate dshipped
on s.[ShippedDate] = dshipped.[Date]

);


