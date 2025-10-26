# TASK 03: Training Data Preparation

**Status**: ⬜ Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: None (can be done in parallel with TASK 01-02)
**Phase**: 2 - Training Data & Knowledge Base

---

## OVERVIEW

Prepare comprehensive training data for the Chinook database including DDL schemas, documentation, and Q&A pairs in both English and Japanese.

**Reference**: PRD Section 4.4

---

## OBJECTIVES

1. Create folder structure for training data
2. Extract and document Chinook database DDL
3. Write table documentation (EN/JP)
4. Create Q&A training pairs (EN/JP, ≥50 examples)
5. Cover various query complexity levels

---

## FOLDER STRUCTURE

```
training_data/
└── chinook/
    ├── README.md                    # Overview of training data
    ├── ddl/                         # DDL files
    │   ├── 01_Album.sql
    │   ├── 02_Artist.sql
    │   ├── 03_Customer.sql
    │   ├── 04_Employee.sql
    │   ├── 05_Genre.sql
    │   ├── 06_Invoice.sql
    │   ├── 07_InvoiceLine.sql
    │   ├── 08_MediaType.sql
    │   ├── 09_Playlist.sql
    │   ├── 10_PlaylistTrack.sql
    │   └── 11_Track.sql
    ├── documentation/               # Table documentation
    │   ├── Album.md
    │   ├── Artist.md
    │   ├── Customer.md
    │   ├── Employee.md
    │   ├── Genre.md
    │   ├── Invoice.md
    │   ├── InvoiceLine.md
    │   ├── MediaType.md
    │   ├── Playlist.md
    │   ├── PlaylistTrack.md
    │   └── Track.md
    └── questions/                   # Q&A pairs (JSON)
        ├── 01_simple_counts.json
        ├── 02_simple_filters.json
        ├── 03_joins.json
        ├── 04_aggregations.json
        ├── 05_complex_queries.json
        └── 06_japanese_queries.json
```

---

## IMPLEMENTATION STEPS

### Step 1: Create Folder Structure

```bash
mkdir -p training_data/chinook/{ddl,documentation,questions}
```

### Step 2: Extract DDL Files

Example `training_data/chinook/ddl/03_Customer.sql`:

```sql
CREATE TABLE Customer (
    CustomerId INTEGER PRIMARY KEY,
    FirstName NVARCHAR(40) NOT NULL,
    LastName NVARCHAR(20) NOT NULL,
    Company NVARCHAR(80),
    Address NVARCHAR(70),
    City NVARCHAR(40),
    State NVARCHAR(40),
    Country NVARCHAR(40),
    PostalCode NVARCHAR(10),
    Phone NVARCHAR(24),
    Fax NVARCHAR(24),
    Email NVARCHAR(60) NOT NULL,
    SupportRepId INTEGER,
    FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
);
```

Create similar files for all 11 tables.

### Step 3: Write Documentation Files

Example `training_data/chinook/documentation/Customer.md`:

```markdown
# Customer Table

## Description
Stores customer information including contact details and assigned support representative.

## 説明 (Japanese)
顧客情報（連絡先と担当サポート担当者を含む）を保存します。

## Columns

- **CustomerId** (INTEGER): Primary key, unique customer identifier
- **FirstName** (NVARCHAR): Customer's first name
- **LastName** (NVARCHAR): Customer's last name
- **Email** (NVARCHAR): Customer email address
- **SupportRepId** (INTEGER): Foreign key to Employee table (support rep)

## Common Queries

- Count total customers
- Find customers by country
- Get customers with their support rep
- Find customers without purchases

## Business Context

Customers are individuals who purchase music from the store. Each customer may be assigned a support representative (Employee).
```

### Step 4: Create Q&A JSON Files

Example `training_data/chinook/questions/01_simple_counts.json`:

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
    "question": "How many albums are in the database?",
    "sql": "SELECT COUNT(*) FROM Album"
  },
  {
    "question": "アルバムは何枚ありますか？",
    "sql": "SELECT COUNT(*) FROM Album"
  },
  {
    "question": "Total number of tracks",
    "sql": "SELECT COUNT(*) FROM Track"
  }
]
```

Example `training_data/chinook/questions/03_joins.json`:

```json
[
  {
    "question": "Show customers with their support representative names",
    "sql": "SELECT c.FirstName || ' ' || c.LastName AS Customer, e.FirstName || ' ' || e.LastName AS SupportRep FROM Customer c LEFT JOIN Employee e ON c.SupportRepId = e.EmployeeId"
  },
  {
    "question": "List all albums with their artist names",
    "sql": "SELECT a.Title AS Album, ar.Name AS Artist FROM Album a JOIN Artist ar ON a.ArtistId = ar.ArtistId"
  },
  {
    "question": "Show tracks with their album and artist",
    "sql": "SELECT t.Name AS Track, al.Title AS Album, ar.Name AS Artist FROM Track t JOIN Album al ON t.AlbumId = al.AlbumId JOIN Artist ar ON al.ArtistId = ar.ArtistId"
  }
]
```

### Step 5: Create README

`training_data/chinook/README.md`:

```markdown
# Chinook Training Data

Training data for Detomo SQL AI on Chinook database.

## Contents

- **ddl/**: Database schema (CREATE TABLE statements)
- **documentation/**: Table descriptions and business context
- **questions/**: Q&A pairs for training (English + Japanese)

## Statistics

- Tables: 11
- DDL files: 11
- Documentation files: 11
- Q&A pairs: 50+
- Languages: English, Japanese

## Usage

```python
from scripts.train_chinook import train_chinook_database
train_chinook_database()
```

## Categories

### Simple Queries (01_simple_counts, 02_simple_filters)
- Count queries
- Simple WHERE clauses
- Single table queries

### Joins (03_joins)
- 2-table joins
- 3-table joins
- LEFT/INNER joins

### Aggregations (04_aggregations)
- GROUP BY
- SUM, AVG, COUNT
- HAVING clauses

### Complex (05_complex_queries)
- Subqueries
- Window functions
- Complex business logic

### Japanese (06_japanese_queries)
- All categories in Japanese
- Natural Japanese phrasing
```

---

## SUCCESS CRITERIA

- [ ] Folder structure created
- [ ] All 11 DDL files created
- [ ] All 11 documentation files created (bilingual)
- [ ] ≥50 Q&A pairs across 6 JSON files
- [ ] Coverage of query types: counts, filters, joins, aggregations, complex
- [ ] Bilingual support (English + Japanese)
- [ ] README.md with overview

---

## DELIVERABLES

1. Complete folder structure
2. 11 DDL files (one per table)
3. 11 documentation files (one per table, bilingual)
4. 6 Q&A JSON files with ≥50 total examples
5. README.md

---

## REFERENCES

- **Chinook Database**: https://github.com/lerocha/chinook-database
- **PRD Section 3.2**: User Flows
- **PRD Section 4.4**: Training Data Management

---

**Last Updated**: 2025-10-26
