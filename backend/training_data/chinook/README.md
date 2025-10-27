# Chinook Training Data

Training data for Detomo SQL AI on the Chinook database - a sample database representing a digital media store.

## Overview

This directory contains comprehensive training data to teach the Detomo SQL AI system how to:
- Understand the Chinook database schema
- Generate accurate SQL queries from natural language questions
- Support both English and Japanese language queries

## Contents

### 1. DDL Files (`ddl/`)

Database schema definitions (CREATE TABLE statements) for all 11 core tables:

- `albums.sql` - Album information
- `artists.sql` - Artist information
- `customers.sql` - Customer details and contact info
- `employees.sql` - Employee records and hierarchy
- `genres.sql` - Music genre classifications
- `invoices.sql` - Customer invoice records
- `invoice_items.sql` - Line items for each invoice
- `media_types.sql` - Media format types (MP3, AAC, etc.)
- `playlists.sql` - User-created playlists
- `playlist_track.sql` - Track-to-playlist associations
- `tracks.sql` - Individual music tracks
- `relationships.sql` - Foreign key relationships

**Total: 12 files**

### 2. Documentation (`documentation/`)

Detailed table documentation with:
- English and Japanese descriptions
- Column definitions and constraints
- Relationship diagrams
- Business rules
- Common query patterns
- Japanese terminology

Documentation files:
- `albums.md`
- `artists.md`
- `customers.md`
- `employees.md`
- `genres.md`
- `invoices.md`
- `invoice_items.md`
- `media_types.md`
- `playlists.md`
- `tracks.md`
- `business_rules.md` - Overall business logic and rules

**Total: 11 files**

### 3. Q&A Pairs (`questions/`)

Training question-answer pairs in JSON format covering various SQL query patterns:

#### `basic_queries.json` (20 pairs)
- Simple COUNT queries
- Single table SELECT queries
- Basic WHERE clause filtering
- Simple sorting and limiting

Example:
```json
{
  "question": "How many customers are there?",
  "sql": "SELECT COUNT(*) FROM customers"
}
```

#### `join_queries.json` (15 pairs)
- 2-table joins (albums with artists)
- 3-table joins (tracks with albums and artists)
- LEFT JOIN patterns
- Customer-employee relationships

Example:
```json
{
  "question": "List albums with artist names",
  "sql": "SELECT al.Title as Album, ar.Name as Artist FROM albums al JOIN artists ar ON al.ArtistId = ar.ArtistId ORDER BY ar.Name"
}
```

#### `aggregation_queries.json` (15 pairs)
- GROUP BY queries
- SUM, AVG, COUNT, MAX aggregations
- HAVING clauses
- Revenue and sales analytics

Example:
```json
{
  "question": "Revenue by country",
  "sql": "SELECT BillingCountry, SUM(Total) as Revenue FROM invoices GROUP BY BillingCountry ORDER BY Revenue DESC"
}
```

#### `japanese_queries.json` (20 pairs)
- All query types in Japanese
- Natural Japanese phrasing
- Common business questions in Japanese
- Bilingual SQL support

Example:
```json
{
  "question": "顧客は何人いますか？",
  "sql": "SELECT COUNT(*) FROM customers"
}
```

**Total: 70 Q&A pairs**

## Statistics

| Category | Count |
|----------|-------|
| Tables | 11 |
| DDL Files | 12 |
| Documentation Files | 11 |
| Q&A Pairs (Total) | 70 |
| Languages Supported | English, Japanese |

## Query Coverage

### Query Complexity Distribution

- **Simple Queries** (20 pairs): Basic counts, filters, single table queries
- **Join Queries** (15 pairs): Multi-table relationships, complex joins
- **Aggregations** (15 pairs): GROUP BY, analytics, revenue calculations
- **Japanese Queries** (20 pairs): All types in Japanese language

### Query Type Categories

1. **Counting & Statistics**
   - Total counts (customers, tracks, albums, etc.)
   - Aggregated statistics (avg, max, min)

2. **Filtering & Selection**
   - Country-based filtering
   - Genre-based filtering
   - Price-based filtering

3. **Joins & Relationships**
   - Album-Artist relationships
   - Customer-Invoice relationships
   - Employee-Customer assignments
   - Track-Playlist associations

4. **Business Analytics**
   - Revenue by country/city
   - Top customers by spending
   - Popular genres and artists
   - Sales performance metrics

5. **Complex Queries**
   - Multi-table joins (3+ tables)
   - Subqueries
   - Time-based analysis
   - Ranking and top-N queries

## Usage

### Loading Training Data

Use the training script to load this data into the DetomoVanna system:

```python
from scripts.train_chinook import train_chinook_database

# Load all training data
train_chinook_database()
```

### Verifying Training Data

```python
from src.detomo_vanna import DetomoVanna

vn = DetomoVanna(config={'path': './detomo_vectordb'})

# Check loaded training data count
training_data = vn.get_training_data()
print(f"Total training items: {len(training_data)}")
```

## Data Quality Standards

All training data follows these quality standards:

✅ **Accuracy**: SQL queries tested against actual Chinook database
✅ **Bilingual**: English and Japanese support throughout
✅ **Comprehensive**: Covers all 11 tables and major query patterns
✅ **Well-documented**: Clear descriptions and business context
✅ **Consistent**: Follows SQLite syntax and Chinook schema conventions

## Chinook Database Schema Overview

The Chinook database represents a digital media store with the following key entities:

- **Artists** create **Albums**
- **Albums** contain **Tracks**
- **Tracks** have **Genres** and **Media Types**
- **Customers** place **Invoices**
- **Invoices** contain **Invoice Items** (purchased tracks)
- **Employees** support **Customers**
- **Tracks** can belong to **Playlists**

## Languages

### English
All documentation and queries include English versions for international users.

### Japanese (日本語)
Complete Japanese language support including:
- Japanese question phrasing (20 Q&A pairs)
- Japanese terminology in documentation
- Natural Japanese business queries

## References

- **Chinook Database**: https://github.com/lerocha/chinook-database
- **Vanna AI Documentation**: https://vanna.ai/docs/
- **Detomo SQL AI PRD**: See `docs/PRD.md`

## Maintenance

This training data should be updated when:
- New query patterns are identified
- SQL accuracy issues are found
- Additional languages need to be supported
- Database schema changes occur

## Version History

- **v1.0** (2025-10-26): Initial training data creation
  - 70 Q&A pairs across 4 categories
  - 11 table documentation files
  - 12 DDL schema files
  - Bilingual support (EN/JP)

---

**Last Updated**: 2025-10-26
**Status**: Complete
**Quality**: Production-ready
