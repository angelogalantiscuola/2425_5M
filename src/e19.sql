-- Exercise: Simple SQL Queries
-- Using the Northwind Demo Database

-- Get all columns from the tables Customers, Orders and Suppliers
SELECT * FROM Customers;
SELECT * FROM Orders;
SELECT * FROM Suppliers;

-- Get all Customers alphabetically, by Country and name
SELECT *
FROM Customers
ORDER BY Country, CompanyName;

-- Get all Orders by date
SELECT *
FROM Orders
ORDER BY OrderDate;

-- Get the count of all Orders made during 1997
SELECT COUNT(*) as OrderCount
FROM Orders
WHERE OrderDate LIKE '2017%';
-- WHERE sztrftime('%Y', OrderDate) = '2016';

-- Get the names of all the contact persons where the person is a manager, alphabetically
SELECT ContactName, ContactTitle
FROM Customers
WHERE ContactTitle LIKE '%Manager%'
ORDER BY ContactName;

-- Get all orders placed on the 19th of May, 1997
SELECT *
FROM Orders
WHERE date(OrderDate) = '1997-05-19';

-- Exercise: SQL Queries for JOINS

-- Create a report for all the orders of 1996 and their Customers (152 rows)
SELECT o.*, c.CompanyName, c.ContactName
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE strftime('%Y', o.OrderDate) = '2016';

-- Create a report that shows the number of employees and customers from each city that has employees in it (5 rows)
SELECT e.City,
    COUNT(DISTINCT e.EmployeeID) as EmployeeCount,
    COUNT(DISTINCT c.CustomerID) as CustomerCount
FROM Employees e
LEFT JOIN Customers c ON e.City = c.City
GROUP BY e.City;


-- Create a report that shows the number of employees and customers from each city that has customers in it (69 rows)
SELECT c.City,
    COUNT(DISTINCT e.EmployeeID) as EmployeeCount,
    COUNT(DISTINCT CustomerID) as CustomerCount
FROM Customers c
LEFT JOIN Employees e ON c.City = e.City
GROUP BY c.City;

-- Create a report that shows the number of employees and customers from each city
SELECT c.City,
    COUNT(DISTINCT e.EmployeeID) as EmployeeCount,
    COUNT(DISTINCT c.CustomerID) as CustomerCount
FROM Customers c
FULL OUTER JOIN Employees e ON c.City = e.City
GROUP BY c.City;

-- Exercise: SQL Queries for HAVING

-- Create a report that shows the order ids and the associated employee names for orders that shipped after the required date (37 rows)
SELECT o.OrderID,
       e.FirstName || ' ' || e.LastName as EmployeeName
FROM Orders o
JOIN Employees e ON o.EmployeeID = e.EmployeeID
WHERE o.ShippedDate > o.RequiredDate;

-- Create a report that shows the total quantity of products ordered where the quantity is fewer than 200
SELECT od.ProductID,
       p.ProductName,
       SUM(od.Quantity) as TotalQuantity
FROM "Order Details" od
JOIN Products p ON od.ProductID = p.ProductID
GROUP BY od.ProductID, p.ProductName
HAVING SUM(od.Quantity) < 200000;


-- Create a report that shows the total number of orders by Customer since December 31,1996 with more than 15 orders (5 rows)
SELECT o.OrderDate,
       c.CustomerID,
       c.CompanyName,
       COUNT(o.OrderID) as OrderCount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE o.OrderDate > '2017-12-31'
GROUP BY c.CustomerID, c.CompanyName
HAVING COUNT(o.OrderID) > 15;

-- Exercise: SQL Inserting Records
-- Using transactions as specified

BEGIN TRANSACTION;

-- Insert into Employees
INSERT INTO Employees (LastName, FirstName, Title, TitleOfCourtesy, BirthDate, HireDate, 
                      City, Region, PostalCode, Country, HomePhone, ReportsTo)
VALUES ('Smith', 'John', 'Sales Representative', 'Mr.', '1990-01-01', CURRENT_DATE,
        'Berlin', NULL, '12209', 'Germany', '(030) 0074321', 5);

-- Insert into Orders
INSERT INTO Orders (CustomerID, EmployeeID, OrderDate, RequiredDate)
VALUES ('VINET', (SELECT EmployeeID FROM Employees WHERE LastName = 'Smith'), 
        CURRENT_DATE, date('now', '+7 days'));

-- Insert into Order_Details
INSERT INTO Order_Details (OrderID, ProductID, UnitPrice, Quantity, Discount)
VALUES ((SELECT MAX(OrderID) FROM Orders), 1, 18.00, 5, 0);

COMMIT;


-- Exercise: SQL Updating Records
-- Using transactions as specified

BEGIN TRANSACTION;

-- Update phone of the employee we just inserted
UPDATE Employees 
SET HomePhone = '(030) 1234567'
WHERE LastName = 'Smith' AND FirstName = 'John';

-- Double the quantity of the order detail we inserted
UPDATE Order_Details
SET Quantity = Quantity * 2
WHERE OrderID = (SELECT MAX(OrderID) FROM Orders)
AND ProductID = 1;

-- Update all orders associated with our employee
UPDATE Order_Details
SET Quantity = Quantity * 2
WHERE OrderID IN (
    SELECT OrderID 
    FROM Orders 
    WHERE EmployeeID = (SELECT EmployeeID FROM Employees WHERE LastName = 'Smith')
);

COMMIT;

-- Exercise: SQL Deleting Records
-- Using transactions as specified

BEGIN TRANSACTION;

-- Delete the records in reverse order of their dependencies
DELETE FROM Order_Details 
WHERE OrderID IN (
    SELECT OrderID 
    FROM Orders 
    WHERE EmployeeID = (SELECT EmployeeID FROM Employees WHERE LastName = 'Smith')
);

DELETE FROM Orders 
WHERE EmployeeID = (SELECT EmployeeID FROM Employees WHERE LastName = 'Smith');

DELETE FROM Employees 
WHERE LastName = 'Smith' AND FirstName = 'John';

COMMIT;


-- Exercise: Advanced SQL Queries

-- What were our total revenues in 1997 (Result must be 617.085,27)
SELECT ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalRevenue
FROM Orders o
JOIN "Order Details" od ON o.OrderID = od.OrderID
WHERE strftime('%Y', o.OrderDate) = '2017';

-- What is the total amount each customer has payed us so far (Hint: QUICK-Stop has payed us 110.277,32)
SELECT 
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalAmount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.CompanyName
ORDER BY c.CompanyName;

-- Find the 10 top selling products (Hint: Top selling product is "Côte de Blaye")
SELECT 
    p.ProductName,
    SUM(od.Quantity) as TotalQuantity,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalRevenue
FROM Products p
JOIN "Order Details" od ON p.ProductID = od.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY TotalRevenue DESC
LIMIT 10;

-- Create a view with total revenues per customer
SELECT 
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalRevenue
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.CompanyName;

-- Which UK Customers have payed us more than 1000 dollars (6 rows)
SELECT 
    c.CustomerID,
    c.CompanyName,
    c.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalAmount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN "Order Details" od ON o.OrderID = od.OrderID
WHERE c.Country = 'UK'
GROUP BY c.CustomerID, c.CompanyName, c.Country
HAVING TotalAmount > 4500000
ORDER BY TotalAmount DESC;

-- How much has each customer payed in total and how much in 1997
SELECT 
    c.CustomerID,
    c.CompanyName,
    c.Country,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) as TotalAllTime,
    ROUND(SUM(
        CASE 
            WHEN strftime('%Y', o.OrderDate) = '2017' 
            THEN od.UnitPrice * od.Quantity * (1 - od.Discount)
            ELSE 0 
        END
    ), 2) as Total1997
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN "Order Details" od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.CompanyName, c.Country
ORDER BY c.CompanyName;
