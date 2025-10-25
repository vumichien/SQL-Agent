# Task 02: Create Training Data Files

**Priority**: HIGH
**Assignee**: Data Engineer / AI Engineer
**Estimate**: 16 hours
**Phase**: Phase 1 - Foundation

---

## Objective
Tạo đầy đủ training data (DDL, Documentation, Q&A pairs) cho Vanna AI để có thể generate SQL queries chính xác từ natural language.

---

## Prerequisites
- Task 01 completed (Chinook database ready)
- Understanding of Chinook database schema
- Knowledge of SQL and database concepts

---

## Directory Structure

```
training_data/
└── chinook/
    ├── ddl/                    # Table definitions
    │   ├── album.sql
    │   ├── artist.sql
    │   ├── customer.sql
    │   ├── employee.sql
    │   ├── genre.sql
    │   ├── invoice.sql
    │   ├── invoice_line.sql
    │   ├── media_type.sql
    │   ├── playlist.sql
    │   ├── playlist_track.sql
    │   ├── track.sql
    │   └── relationships.sql
    ├── documentation/          # Table documentation
    │   ├── album.md
    │   ├── artist.md
    │   ├── customer.md
    │   ├── employee.md
    │   ├── genre.md
    │   ├── invoice.md
    │   ├── invoice_line.md
    │   ├── media_type.md
    │   ├── playlist.md
    │   ├── track.md
    │   └── business_rules.md
    └── questions/              # Q&A pairs
        ├── basic_queries.json
        ├── aggregation_queries.json
        ├── join_queries.json
        └── japanese_queries.json
```

---

## Steps

### Step 1: Create Directory Structure (30 min)
```bash
mkdir -p training_data/chinook/{ddl,documentation,questions}
```

### Step 2: Extract DDL Files (2 hours)

Tạo separate DDL file cho mỗi table.

**Example: `training_data/chinook/ddl/customer.sql`**
```sql
CREATE TABLE Customer (
    CustomerId INTEGER PRIMARY KEY,
    FirstName VARCHAR(40) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Email VARCHAR(60) NOT NULL,
    Company VARCHAR(80),
    Address VARCHAR(70),
    City VARCHAR(40),
    State VARCHAR(40),
    Country VARCHAR(40),
    PostalCode VARCHAR(10),
    Phone VARCHAR(24),
    Fax VARCHAR(24),
    SupportRepId INTEGER,
    FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
);
```

**Extract command**:
```sql
-- Connect to database
psql -U postgres -d chinook

-- Get DDL for each table
\d+ Customer
```

Repeat for all 11 tables:
- [ ] album.sql
- [ ] artist.sql
- [ ] customer.sql
- [ ] employee.sql
- [ ] genre.sql
- [ ] invoice.sql
- [ ] invoice_line.sql
- [ ] media_type.sql
- [ ] playlist.sql
- [ ] playlist_track.sql
- [ ] track.sql

### Step 3: Create Relationships File (1 hour)

**File: `training_data/chinook/ddl/relationships.sql`**
```sql
-- Foreign Key Relationships in Chinook Database

-- Album -> Artist
ALTER TABLE Album ADD CONSTRAINT FK_Album_Artist
    FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId);

-- Customer -> Employee (Support Rep)
ALTER TABLE Customer ADD CONSTRAINT FK_Customer_Employee
    FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId);

-- Employee -> Employee (Reports To)
ALTER TABLE Employee ADD CONSTRAINT FK_Employee_Employee
    FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId);

-- Invoice -> Customer
ALTER TABLE Invoice ADD CONSTRAINT FK_Invoice_Customer
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId);

-- InvoiceLine -> Invoice
ALTER TABLE InvoiceLine ADD CONSTRAINT FK_InvoiceLine_Invoice
    FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId);

-- InvoiceLine -> Track
ALTER TABLE InvoiceLine ADD CONSTRAINT FK_InvoiceLine_Track
    FOREIGN KEY (TrackId) REFERENCES Track(TrackId);

-- PlaylistTrack -> Playlist
ALTER TABLE PlaylistTrack ADD CONSTRAINT FK_PlaylistTrack_Playlist
    FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId);

-- PlaylistTrack -> Track
ALTER TABLE PlaylistTrack ADD CONSTRAINT FK_PlaylistTrack_Track
    FOREIGN KEY (TrackId) REFERENCES Track(TrackId);

-- Track -> Album
ALTER TABLE Track ADD CONSTRAINT FK_Track_Album
    FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId);

-- Track -> Genre
ALTER TABLE Track ADD CONSTRAINT FK_Track_Genre
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId);

-- Track -> MediaType
ALTER TABLE Track ADD CONSTRAINT FK_Track_MediaType
    FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId);
```

### Step 4: Write Documentation Files (8 hours)

Document each table with:
- Description
- Column details
- Business rules
- Sample queries
- Relationships

**Example: `training_data/chinook/documentation/customer.md`**
```markdown
# Customer Table

## Description
Stores customer information for the digital music store. Each customer can place multiple orders (invoices) and is assigned to a support representative.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CustomerId | INTEGER | PRIMARY KEY | Unique customer identifier |
| FirstName | VARCHAR(40) | NOT NULL | Customer first name |
| LastName | VARCHAR(20) | NOT NULL | Customer last name |
| Email | VARCHAR(60) | NOT NULL | Email address (unique) |
| Company | VARCHAR(80) | | Company name (optional) |
| Address | VARCHAR(70) | | Street address |
| City | VARCHAR(40) | | City |
| State | VARCHAR(40) | | State/Province |
| Country | VARCHAR(40) | | Country |
| PostalCode | VARCHAR(10) | | Postal/ZIP code |
| Phone | VARCHAR(24) | | Phone number |
| Fax | VARCHAR(24) | | Fax number |
| SupportRepId | INTEGER | FOREIGN KEY | Reference to Employee (support rep) |

## Relationships

**One-to-Many**:
- One Customer → Many Invoices
- One Employee (Support Rep) → Many Customers

## Business Rules

1. Email must be unique across all customers
2. FirstName and LastName are required
3. Each customer is assigned to ONE support representative
4. SupportRepId references Employee with Title = 'Sales Support Agent'
5. Customer can have ZERO or MORE invoices

## Common Query Patterns

### Count customers
```sql
SELECT COUNT(*) FROM Customer;
```

### Get customers by country
```sql
SELECT * FROM Customer WHERE Country = 'USA';
```

### Find customer's total spending
```sql
SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    SUM(i.Total) as TotalSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY TotalSpent DESC;
```

## Japanese Terminology
- 顧客 (kokyaku) = Customer
- 売上 (uriage) = Sales/Revenue
- 請求書 (seikyusho) = Invoice
```

Create documentation for all tables:
- [ ] customer.md
- [ ] invoice.md
- [ ] invoice_line.md
- [ ] track.md
- [ ] album.md
- [ ] artist.md
- [ ] genre.md
- [ ] playlist.md
- [ ] employee.md
- [ ] media_type.md
- [ ] business_rules.md

### Step 5: Create Q&A Pairs (6 hours)

#### 5.1 Basic Queries (20 questions)
**File: `training_data/chinook/questions/basic_queries.json`**
```json
[
  {
    "question": "How many customers are there?",
    "sql": "SELECT COUNT(*) FROM Customer"
  },
  {
    "question": "顧客は何人いますか？",
    "sql": "SELECT COUNT(*) FROM Customer"
  },
  {
    "question": "List first 10 customers",
    "sql": "SELECT * FROM Customer LIMIT 10"
  },
  {
    "question": "最初の10人の顧客をリストしてください",
    "sql": "SELECT * FROM Customer LIMIT 10"
  },
  {
    "question": "How many customers are from USA?",
    "sql": "SELECT COUNT(*) FROM Customer WHERE Country = 'USA'"
  },
  {
    "question": "Show all genres",
    "sql": "SELECT * FROM Genre ORDER BY Name"
  },
  {
    "question": "すべての音楽ジャンルを表示",
    "sql": "SELECT * FROM Genre ORDER BY Name"
  },
  {
    "question": "How many tracks are there?",
    "sql": "SELECT COUNT(*) FROM Track"
  },
  {
    "question": "List all artists",
    "sql": "SELECT * FROM Artist ORDER BY Name"
  },
  {
    "question": "Get all albums",
    "sql": "SELECT * FROM Album ORDER BY Title"
  }
]
```

#### 5.2 Aggregation Queries (15 questions)
**File: `training_data/chinook/questions/aggregation_queries.json`**
```json
[
  {
    "question": "What is the total revenue?",
    "sql": "SELECT SUM(Total) as TotalRevenue FROM Invoice"
  },
  {
    "question": "総売上はいくらですか？",
    "sql": "SELECT SUM(Total) as TotalRevenue FROM Invoice"
  },
  {
    "question": "Revenue by country",
    "sql": "SELECT BillingCountry, SUM(Total) as Revenue FROM Invoice GROUP BY BillingCountry ORDER BY Revenue DESC"
  },
  {
    "question": "国別の売上",
    "sql": "SELECT BillingCountry, SUM(Total) as Revenue FROM Invoice GROUP BY BillingCountry ORDER BY Revenue DESC"
  },
  {
    "question": "Top 10 customers by spending",
    "sql": "SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId, c.FirstName, c.LastName ORDER BY TotalSpent DESC LIMIT 10"
  },
  {
    "question": "売上トップ10の顧客",
    "sql": "SELECT c.FirstName, c.LastName, SUM(i.Total) as TotalSpent FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId, c.FirstName, c.LastName ORDER BY TotalSpent DESC LIMIT 10"
  },
  {
    "question": "Average invoice total",
    "sql": "SELECT AVG(Total) as AverageInvoice FROM Invoice"
  },
  {
    "question": "Most popular genre by sales",
    "sql": "SELECT g.Name, COUNT(il.InvoiceLineId) as TimesSold FROM Genre g JOIN Track t ON g.GenreId = t.GenreId JOIN InvoiceLine il ON t.TrackId = il.TrackId GROUP BY g.Name ORDER BY TimesSold DESC LIMIT 1"
  }
]
```

#### 5.3 Join Queries (15 questions)
**File: `training_data/chinook/questions/join_queries.json`**
```json
[
  {
    "question": "List albums with artist names",
    "sql": "SELECT al.Title as Album, ar.Name as Artist FROM Album al JOIN Artist ar ON al.ArtistId = ar.ArtistId ORDER BY ar.Name"
  },
  {
    "question": "アルバムとアーティストをリストしてください",
    "sql": "SELECT al.Title as Album, ar.Name as Artist FROM Album al JOIN Artist ar ON al.ArtistId = ar.ArtistId ORDER BY ar.Name"
  },
  {
    "question": "Show tracks with album and artist",
    "sql": "SELECT t.Name as Track, al.Title as Album, ar.Name as Artist FROM Track t JOIN Album al ON t.AlbumId = al.AlbumId JOIN Artist ar ON al.ArtistId = ar.ArtistId"
  },
  {
    "question": "Customer invoices with details",
    "sql": "SELECT c.FirstName, c.LastName, i.InvoiceId, i.InvoiceDate, i.Total FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId ORDER BY i.InvoiceDate DESC"
  },
  {
    "question": "Employees and their customers",
    "sql": "SELECT e.FirstName as EmployeeName, e.LastName as EmployeeLastName, COUNT(c.CustomerId) as CustomerCount FROM Employee e LEFT JOIN Customer c ON e.EmployeeId = c.SupportRepId GROUP BY e.EmployeeId, e.FirstName, e.LastName"
  }
]
```

#### 5.4 Japanese Queries (20 questions)
**File: `training_data/chinook/questions/japanese_queries.json`**
```json
[
  {
    "question": "2024年の月別総売上",
    "sql": "SELECT DATE_TRUNC('month', InvoiceDate) as Month, SUM(Total) as Revenue FROM Invoice WHERE EXTRACT(YEAR FROM InvoiceDate) = 2024 GROUP BY Month ORDER BY Month"
  },
  {
    "question": "最も売れている音楽ジャンルは？",
    "sql": "SELECT g.Name, COUNT(il.InvoiceLineId) as TimesSold FROM Genre g JOIN Track t ON g.GenreId = t.GenreId JOIN InvoiceLine il ON t.TrackId = il.TrackId GROUP BY g.Name ORDER BY TimesSold DESC LIMIT 1"
  },
  {
    "question": "従業員の一覧",
    "sql": "SELECT FirstName, LastName, Title FROM Employee ORDER BY LastName"
  },
  {
    "question": "ロックジャンルのトラック数",
    "sql": "SELECT COUNT(*) FROM Track t JOIN Genre g ON t.GenreId = g.GenreId WHERE g.Name = 'Rock'"
  }
]
```

---

## Verification Checklist

### DDL Files
- [ ] All 11 table DDL files created
- [ ] Relationships file created
- [ ] DDL syntax is valid PostgreSQL
- [ ] Foreign key constraints documented

### Documentation Files
- [ ] All 10 table documentation files created
- [ ] Business rules documented
- [ ] Each file has: description, columns, relationships, sample queries
- [ ] Japanese terminology included

### Q&A Files
- [ ] basic_queries.json (20 questions)
- [ ] aggregation_queries.json (15 questions)
- [ ] join_queries.json (15 questions)
- [ ] japanese_queries.json (20 questions)
- [ ] Total: 70 Q&A pairs
- [ ] All SQL queries are valid
- [ ] Mix of English and Japanese questions

### Quality Check
- [ ] All SQL queries tested and working
- [ ] Japanese characters properly encoded (UTF-8)
- [ ] JSON files are valid
- [ ] No syntax errors
- [ ] Consistent formatting

---

## Output/Deliverables

- ✅ 11 DDL files + 1 relationships file
- ✅ 10 documentation files + 1 business rules file
- ✅ 4 Q&A JSON files with 70+ question-answer pairs
- ✅ All files UTF-8 encoded
- ✅ All SQL queries validated

---

## Next Task
➡️ [Task 03: Implement DetomoVanna Class](TASK_03_implement_detomo_vanna.md)

---

## Tips

1. **DDL Extraction**: Use `pg_dump` for accurate DDL
   ```bash
   pg_dump -U postgres -d chinook --schema-only -t Customer
   ```

2. **Test SQL Queries**: Always test in psql before adding to JSON
   ```bash
   psql -U postgres -d chinook -f test_query.sql
   ```

3. **JSON Validation**: Use online validators or jq
   ```bash
   cat basic_queries.json | jq .
   ```

4. **Encoding**: Ensure UTF-8 for Japanese characters
   ```bash
   file -bi japanese_queries.json
   ```

---

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Blocked (reason: _________________)
- [ ] Completed
- [ ] Verified

**Completed Date**: __________
**Completed By**: __________
