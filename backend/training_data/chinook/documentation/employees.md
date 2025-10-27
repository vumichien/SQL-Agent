# Employees Table

## Description
Stores employee information including sales support representatives. Contains self-referencing relationship for manager hierarchy.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| EmployeeId | INTEGER | PRIMARY KEY | Unique employee identifier |
| LastName | NVARCHAR(20) | NOT NULL | Employee last name |
| FirstName | NVARCHAR(20) | NOT NULL | Employee first name |
| Title | NVARCHAR(30) | | Job title |
| ReportsTo | INTEGER | FOREIGN KEY | Reference to manager (Employee) |
| BirthDate | DATETIME | | Date of birth |
| HireDate | DATETIME | | Date hired |
| Address | NVARCHAR(70) | | Street address |
| City | NVARCHAR(40) | | City |
| State | NVARCHAR(40) | | State/Province |
| Country | NVARCHAR(40) | | Country |
| PostalCode | NVARCHAR(10) | | Postal code |
| Phone | NVARCHAR(24) | | Phone number |
| Fax | NVARCHAR(24) | | Fax number |
| Email | NVARCHAR(60) | | Email address |

## Relationships

**Self-Referencing**:
- One Employee (Manager) → Many Employees (Direct Reports)

**One-to-Many**:
- One Employee (Support Rep) → Many Customers

## Business Rules

1. FirstName and LastName are required
2. ReportsTo creates manager hierarchy
3. Top-level managers have NULL ReportsTo
4. Employees with Title 'Sales Support Agent' can be assigned to customers

## Common Query Patterns

### List all employees
```sql
SELECT FirstName, LastName, Title FROM employees ORDER BY LastName;
```

### Employees with their managers
```sql
SELECT
    e.FirstName || ' ' || e.LastName as Employee,
    m.FirstName || ' ' || m.LastName as Manager
FROM employees e
LEFT JOIN employees m ON e.ReportsTo = m.EmployeeId;
```

### Support reps with customer count
```sql
SELECT
    e.FirstName || ' ' || e.LastName as SupportRep,
    COUNT(c.CustomerId) as CustomerCount
FROM employees e
LEFT JOIN customers c ON e.EmployeeId = c.SupportRepId
GROUP BY e.EmployeeId, e.FirstName, e.LastName;
```

## Japanese Terminology
- 従業員 (juugyouin) = Employee
- 上司 (joushi) = Manager/Supervisor
- 職位 (shokui) = Title/Position
- 採用日 (saiyou bi) = Hire date
