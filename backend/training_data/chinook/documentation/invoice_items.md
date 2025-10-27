# Invoice Items Table

## Description
Stores line items for each invoice. Each row represents one track purchased in an invoice.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| InvoiceLineId | INTEGER | PRIMARY KEY | Unique invoice line item identifier |
| InvoiceId | INTEGER | NOT NULL, FOREIGN KEY | Reference to Invoice |
| TrackId | INTEGER | NOT NULL, FOREIGN KEY | Reference to Track |
| UnitPrice | NUMERIC(10,2) | NOT NULL | Price per track |
| Quantity | INTEGER | NOT NULL | Number of tracks purchased |

## Relationships

**Many-to-One**:
- Many Invoice Items → One Invoice
- Many Invoice Items → One Track

## Business Rules

1. Each line item belongs to exactly ONE invoice
2. Each line item references exactly ONE track
3. Quantity must be >= 1
4. UnitPrice is the price at time of purchase (may differ from current track price)
5. Line item total = UnitPrice * Quantity

## Common Query Patterns

### Get invoice details with line items
```sql
SELECT
    i.InvoiceId,
    t.Name as TrackName,
    il.UnitPrice,
    il.Quantity,
    (il.UnitPrice * il.Quantity) as LineTotal
FROM invoice_items il
JOIN invoices i ON il.InvoiceId = i.InvoiceId
JOIN tracks t ON il.TrackId = t.TrackId
WHERE i.InvoiceId = 1;
```

### Most sold tracks
```sql
SELECT
    t.Name as Track,
    SUM(il.Quantity) as TotalSold
FROM invoice_items il
JOIN tracks t ON il.TrackId = t.TrackId
GROUP BY t.TrackId, t.Name
ORDER BY TotalSold DESC
LIMIT 10;
```

### Revenue by track
```sql
SELECT
    t.Name,
    SUM(il.UnitPrice * il.Quantity) as Revenue
FROM invoice_items il
JOIN tracks t ON il.TrackId = t.TrackId
GROUP BY t.TrackId, t.Name
ORDER BY Revenue DESC;
```

## Japanese Terminology
- 明細 (meisai) = Line item
- 単価 (tanka) = Unit price
- 数量 (suuryou) = Quantity
- 小計 (shoukai) = Subtotal
