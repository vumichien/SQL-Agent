# Task 01: Verify Chinook Database

**Priority**: HIGH
**Assignee**: Backend Developer
**Estimate**: 30 minutes
**Phase**: Phase 1 - Foundation

---

## Objective
Verify và test Chinook SQLite database có sẵn tại `data/chinook.db` để đảm bảo sẵn sàng sử dụng cho dự án Detomo SQL AI.

---

## Prerequisites
- Python 3.10+ đã được cài đặt (có sẵn sqlite3 module)
- File `data/chinook.db` tồn tại trong project

---

## Database Information

**Type**: SQLite 3.x
**Location**: `data/chinook.db`
**Size**: ~884 KB
**Tables**: 11 tables

### Table Structure:
- `albums` (347 rows)
- `artists` (275 rows)
- `customers` (59 rows)
- `employees` (8 rows)
- `genres` (25 rows)
- `invoices` (412 rows)
- `invoice_items` (2,240 rows)
- `media_types` (5 rows)
- `playlists` (18 rows)
- `playlist_track` (8,715 rows)
- `tracks` (3,503 rows)

---

## Steps

### 1. Verify Database File Exists
```bash
# Check if file exists
ls -la data/chinook.db

# Expected output:
# -rw-r--r-- 1 user user 884736 Nov 29  2015 data/chinook.db
```

### 2. Test Database Connection
```python
# Test script: test_db_connection.py
import sqlite3

def test_connection():
    try:
        conn = sqlite3.connect('data/chinook.db')
        cursor = conn.cursor()

        # Test simple query
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]
        print(f"✓ Database connected successfully")
        print(f"✓ Customers count: {count}")

        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

**Run test**:
```bash
python test_db_connection.py
```

### 3. Verify All Tables
```python
# Script: verify_tables.py
import sqlite3

def verify_tables():
    conn = sqlite3.connect('data/chinook.db')
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row[0] for row in cursor.fetchall()]

    print("Tables found:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  ✓ {table}: {count:,} rows")

    conn.close()

if __name__ == "__main__":
    verify_tables()
```

**Run verification**:
```bash
python verify_tables.py
```

**Expected output**:
```
Tables found:
  ✓ albums: 347 rows
  ✓ artists: 275 rows
  ✓ customers: 59 rows
  ✓ employees: 8 rows
  ✓ genres: 25 rows
  ✓ invoice_items: 2,240 rows
  ✓ invoices: 412 rows
  ✓ media_types: 5 rows
  ✓ playlist_track: 8,715 rows
  ✓ playlists: 18 rows
  ✓ tracks: 3,503 rows
```

### 4. Test Sample Queries
```python
# Script: test_queries.py
import sqlite3

def test_sample_queries():
    conn = sqlite3.connect('data/chinook.db')
    cursor = conn.cursor()

    print("Testing sample queries:\n")

    # Query 1: Count customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"1. Total customers: {cursor.fetchone()[0]}")

    # Query 2: Top 5 artists by album count
    cursor.execute("""
        SELECT ar.Name, COUNT(al.AlbumId) as album_count
        FROM artists ar
        JOIN albums al ON ar.ArtistId = al.ArtistId
        GROUP BY ar.ArtistId
        ORDER BY album_count DESC
        LIMIT 5
    """)
    print("\n2. Top 5 artists by album count:")
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]} albums")

    # Query 3: Total revenue
    cursor.execute("SELECT SUM(Total) FROM invoices")
    total = cursor.fetchone()[0]
    print(f"\n3. Total revenue: ${total:,.2f}")

    # Query 4: Genre distribution
    cursor.execute("""
        SELECT g.Name, COUNT(t.TrackId) as track_count
        FROM genres g
        JOIN tracks t ON g.GenreId = t.GenreId
        GROUP BY g.GenreId
        ORDER BY track_count DESC
        LIMIT 5
    """)
    print("\n4. Top 5 genres by track count:")
    for row in cursor.fetchall():
        print(f"   - {row[0]}: {row[1]} tracks")

    conn.close()
    print("\n✓ All sample queries executed successfully!")

if __name__ == "__main__":
    test_sample_queries()
```

**Run tests**:
```bash
python test_queries.py
```

### 5. Inspect Database Schema
```python
# Script: inspect_schema.py
import sqlite3

def inspect_schema():
    conn = sqlite3.connect('data/chinook.db')
    cursor = conn.cursor()

    # Get schema for customers table (example)
    cursor.execute("""
        SELECT sql FROM sqlite_master
        WHERE type='table' AND name='customers'
    """)

    schema = cursor.fetchone()[0]
    print("Sample Schema (customers table):")
    print(schema)

    conn.close()

if __name__ == "__main__":
    inspect_schema()
```

### 6. Create Configuration File
Create `.env` file in project root:
```bash
# Database Configuration (SQLite)
DB_TYPE=sqlite
DB_PATH=data/chinook.db

# Note: SQLite doesn't need host, user, password for local file access
```

---

## Verification Checklist

- [ ] File `data/chinook.db` exists
- [ ] Database opens successfully with sqlite3
- [ ] All 11 tables present
- [ ] Row counts match expected values:
  - customers: 59
  - albums: 347
  - artists: 275
  - tracks: 3,503
  - invoices: 412
- [ ] Sample queries execute without errors
- [ ] Can perform JOIN queries
- [ ] Can perform aggregation queries (SUM, COUNT)
- [ ] `.env` file created with DB_PATH
- [ ] All test scripts run successfully

---

## Troubleshooting

### Issue: File not found
**Solution**: Verify file location
```bash
# Check file exists
test -f data/chinook.db && echo "File exists" || echo "File not found"

# If not found, check if in different location
find . -name "chinook.db"
```

### Issue: Database locked
**Solution**: Close all connections to the database
```python
# Make sure to close connections properly
conn = sqlite3.connect('data/chinook.db')
# ... do work ...
conn.close()  # Always close!
```

### Issue: Permission denied
**Solution**: Check file permissions
```bash
# Check permissions
ls -la data/chinook.db

# Fix if needed (Linux/Mac)
chmod 644 data/chinook.db
```

### Issue: Encoding errors
**Solution**: SQLite database is UTF-8 encoded, make sure Python uses UTF-8
```python
# Set connection with UTF-8
conn = sqlite3.connect('data/chinook.db')
conn.text_factory = str  # Ensure text is handled as UTF-8
```

---

## Key Differences from PostgreSQL

**Note**: This database is SQLite, not PostgreSQL as originally specified in PRD.

| Feature | PostgreSQL (PRD) | SQLite (Actual) |
|---------|------------------|-----------------|
| Type | Server-based | File-based |
| Connection | Host/Port/User/Password | File path only |
| Deployment | Requires server | Embedded, no server |
| Table names | PascalCase (Album) | lowercase (albums) |
| Module | psycopg2 | sqlite3 (built-in) |

**Vanna supports both**, so we'll adapt the code accordingly.

---

## Output/Deliverables

- ✅ Database verified and accessible
- ✅ All tables confirmed present
- ✅ Sample queries working
- ✅ Test scripts created and passing
- ✅ `.env` file configured for SQLite
- ✅ Schema documentation ready

---

## Next Task
➡️ [Task 02: Create Training Data Files](TASK_02_create_training_data.md)

---

## Resources
- SQLite Documentation: https://www.sqlite.org/docs.html
- Python sqlite3 module: https://docs.python.org/3/library/sqlite3.html
- Chinook Database GitHub: https://github.com/lerocha/chinook-database
- Chinook ERD: https://github.com/lerocha/chinook-database/wiki/Chinook-Schema

---

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Blocked (reason: _________________)
- [ ] Completed
- [ ] Verified

**Completed Date**: __________
**Completed By**: __________
