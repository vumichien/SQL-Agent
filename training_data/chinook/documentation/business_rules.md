# Chinook Database Business Rules

## Overview
This document describes the business rules and constraints for the Chinook digital music store database.

## Entity Rules

### Customers
- Every customer must have FirstName, LastName, and Email
- Customer can be assigned to one support representative (employee)
- Customer can place multiple orders (invoices)
- Customer billing information may differ from their profile address

### Employees
- Employees have hierarchical reporting structure (ReportsTo)
- Sales Support Agents are assigned to customers as support representatives
- Managers can have multiple direct reports

### Artists & Albums
- Every album belongs to exactly one artist
- Artists can have zero or more albums
- Album titles are not unique across different artists

### Tracks
- Every track must have a name and media type
- Tracks optionally belong to an album
- Tracks optionally have a genre
- Track price (UnitPrice) is typically $0.99 or $1.99
- Duration (Milliseconds) must be positive

### Invoices & Payments
- Every invoice belongs to exactly one customer
- Invoice total equals sum of all line items
- Invoice line items reference tracks with price at time of purchase
- Minimum order quantity per line item is 1

### Playlists
- Playlists contain multiple tracks (many-to-many)
- Tracks can appear in multiple playlists
- Playlists are predefined collections (not user-generated)

## Pricing Rules
- Track prices are in USD
- Standard track price: $0.99
- Premium track price: $1.99
- Invoice line items store historical price (may differ from current track price)

## Date Rules
- InvoiceDate cannot be in the future
- HireDate should be after BirthDate for employees
- All dates stored in DATETIME format

## Referential Integrity
- Foreign keys enforce referential integrity
- ON DELETE NO ACTION prevents orphaned records
- Cascading updates not enabled by default

## Query Performance Guidelines
- Use indexes on foreign key columns for JOIN optimization
- Filter by Country, Genre, or Artist for common queries
- Use date ranges for temporal analysis
- Aggregate sales data at invoice level, not line item level for totals

## Revenue Calculations

### Total Revenue
```sql
SELECT SUM(Total) FROM invoices;
```

### Revenue by Period
```sql
SELECT
    strftime('%Y-%m', InvoiceDate) as Month,
    SUM(Total) as Revenue
FROM invoices
GROUP BY Month;
```

### Customer Lifetime Value
```sql
SELECT
    CustomerId,
    SUM(Total) as LifetimeValue
FROM invoices
GROUP BY CustomerId;
```

## Common Business Questions

1. **Top Customers**: Who are our highest spending customers?
2. **Popular Genres**: Which music genres sell best?
3. **Sales Trends**: How do sales vary by month/quarter/year?
4. **Artist Performance**: Which artists generate most revenue?
5. **Geographic Analysis**: Which countries/cities have highest sales?
6. **Support Rep Performance**: How many customers per support rep?
7. **Product Mix**: What's the distribution of track sales by genre/media type?

## Data Quality Rules
- Email addresses should be valid format
- Phone numbers should include country code for international
- Postal codes should match country format
- No negative prices or quantities
- No future invoice dates

## Japanese Business Terminology
- 売上高 (uriage daka) = Total sales/revenue
- 顧客生涯価値 (kokyaku shougai kachi) = Customer lifetime value
- 月次売上 (getsuji uriage) = Monthly sales
- トップ顧客 (toppu kokyaku) = Top customers
- 販売実績 (hanbai jisseki) = Sales performance
- 地域分析 (chiiki bunseki) = Geographic analysis
