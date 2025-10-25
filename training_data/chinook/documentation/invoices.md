# Invoices Table

## Description
Stores customer purchase orders. Each invoice represents a single transaction and can contain multiple line items (tracks purchased).

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| InvoiceId | INTEGER | PRIMARY KEY | Unique invoice identifier |
| CustomerId | INTEGER | NOT NULL, FOREIGN KEY | Reference to Customer |
| InvoiceDate | DATETIME | NOT NULL | Date and time of purchase |
| BillingAddress | NVARCHAR(70) | | Billing street address |
| BillingCity | NVARCHAR(40) | | Billing city |
| BillingState | NVARCHAR(40) | | Billing state/province |
| BillingCountry | NVARCHAR(40) | | Billing country |
| BillingPostalCode | NVARCHAR(10) | | Billing postal code |
| Total | NUMERIC(10,2) | NOT NULL | Total invoice amount |

## Relationships

**One-to-Many**:
- One Customer → Many Invoices
- One Invoice → Many Invoice Items (line items)

## Business Rules

1. Every invoice must belong to a customer
2. InvoiceDate is required and cannot be in the future
3. Total represents the sum of all invoice line items
4. Billing information can be different from customer's address
5. Total is stored in USD currency

## Common Query Patterns

### Get total revenue
```sql
SELECT SUM(Total) as TotalRevenue FROM invoices;
```

### Revenue by country
```sql
SELECT
    BillingCountry,
    SUM(Total) as Revenue,
    COUNT(*) as InvoiceCount
FROM invoices
GROUP BY BillingCountry
ORDER BY Revenue DESC;
```

### Get customer invoices
```sql
SELECT
    c.FirstName || ' ' || c.LastName as Customer,
    i.InvoiceDate,
    i.Total
FROM invoices i
JOIN customers c ON i.CustomerId = c.CustomerId
ORDER BY i.InvoiceDate DESC;
```

### Monthly revenue
```sql
SELECT
    strftime('%Y-%m', InvoiceDate) as Month,
    SUM(Total) as Revenue
FROM invoices
GROUP BY Month
ORDER BY Month;
```

## Japanese Terminology
- 請求書 (seikyusho) = Invoice
- 売上 (uriage) = Sales/Revenue
- 合計金額 (gokei kingaku) = Total amount
- 請求日 (seikyu bi) = Invoice date
- 請求先 (seikyusaki) = Billing address
