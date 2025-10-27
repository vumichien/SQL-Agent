# Customers Table

## Description
Stores customer information for the digital music store. Each customer can place multiple orders (invoices) and is assigned to a support representative (employee).

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CustomerId | INTEGER | PRIMARY KEY | Unique customer identifier |
| FirstName | NVARCHAR(40) | NOT NULL | Customer first name |
| LastName | NVARCHAR(20) | NOT NULL | Customer last name |
| Company | NVARCHAR(80) | | Company name (optional) |
| Address | NVARCHAR(70) | | Street address |
| City | NVARCHAR(40) | | City |
| State | NVARCHAR(40) | | State/Province |
| Country | NVARCHAR(40) | | Country |
| PostalCode | NVARCHAR(10) | | Postal/ZIP code |
| Phone | NVARCHAR(24) | | Phone number |
| Fax | NVARCHAR(24) | | Fax number |
| Email | NVARCHAR(60) | NOT NULL | Email address |
| SupportRepId | INTEGER | FOREIGN KEY | Reference to Employee (support representative) |

## Relationships

**One-to-Many**:
- One Customer → Many Invoices
- One Employee (Support Rep) → Many Customers

## Business Rules

1. FirstName and LastName are required fields
2. Email is required and should be unique
3. Each customer can be assigned to ONE support representative
4. SupportRepId references an Employee with role 'Sales Support Agent'
5. Customer can have ZERO or MORE invoices

## Common Query Patterns

### Count total customers
```sql
SELECT COUNT(*) FROM customers;
```

### Get customers by country
```sql
SELECT * FROM customers WHERE Country = 'USA';
```

### Find customer's total spending
```sql
SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    SUM(i.Total) as TotalSpent
FROM customers c
JOIN invoices i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalSpent DESC;
```

### Get customers with their support rep
```sql
SELECT
    c.FirstName || ' ' || c.LastName as CustomerName,
    e.FirstName || ' ' || e.LastName as SupportRep
FROM customers c
LEFT JOIN employees e ON c.SupportRepId = e.EmployeeId;
```

## Japanese Terminology
- 顧客 (kokyaku) = Customer
- メール (meeru) = Email
- 住所 (jusho) = Address
- 電話番号 (denwa bango) = Phone number
- サポート担当 (sapooto tantou) = Support representative
