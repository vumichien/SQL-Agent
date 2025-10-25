# Database Updates: PostgreSQL → SQLite

**Date**: 2025-10-25
**Reason**: Chinook database có sẵn là SQLite (data/chinook.db), không phải PostgreSQL

---

## Key Changes

### 1. Database Type
- **Original (PRD)**: PostgreSQL
- **Actual**: SQLite 3.x
- **Impact**: Simplified setup, no server needed

### 2. Table Names
- **PostgreSQL**: PascalCase (Album, Customer, InvoiceLine)
- **SQLite**: lowercase + underscore (albums, customers, invoice_items)

### 3. Connection Method
- **PostgreSQL**: `psycopg2` with host/port/user/password
- **SQLite**: Built-in `sqlite3` module with file path only

---

## Files Updated

### ✅ TASK_01_setup_chinook_database.md
- **Changed**: From "Setup PostgreSQL" to "Verify SQLite Database"
- **Estimate**: Reduced from 2 hours to 30 minutes
- **New Steps**:
  - Verify file exists
  - Test connection with sqlite3
  - Run verification scripts
  - Create .env with DB_PATH

---

## Files That Need Updating

### 📝 TASK_02_create_training_data.md
**Changes needed**:
- Update table names to lowercase
- Update DDL extraction commands
- Use SQLite-specific SQL syntax if needed

### 📝 TASK_03_implement_detomo_vanna.md
**Changes needed**:
- Change from `psycopg2-binary` to `sqlite3` (built-in)
- Update `config.py` for SQLite connection
- Use `vn.connect_to_sqlite()` instead of `vn.connect_to_postgres()`
- Update connection parameters

### 📝 TASK_04_training_script.md
**Changes needed**:
- Update table names in verification queries
- Update connection code

### 📝 PRD.md (Reference only)
**Note**: Keep PRD as-is for historical record, but note the database change in implementation

### 📝 CLAUDE.md
**Changes needed**:
- Update Task 01 execution steps
- Update database connection examples
- Update table names throughout

### 📝 TASK_MASTER.md
**Changes needed**:
- Update Task 01 estimate (2h → 30min)
- Note about SQLite vs PostgreSQL

---

## Configuration Changes

### Old (.env for PostgreSQL):
```bash
DB_HOST=localhost
DB_NAME=chinook
DB_USER=detomo_reader
DB_PASSWORD=your_password
DB_PORT=5432
```

### New (.env for SQLite):
```bash
DB_TYPE=sqlite
DB_PATH=data/chinook.db
```

---

## Code Changes Required

### config.py
```python
# Old (PostgreSQL)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "chinook")
DB_USER = os.getenv("DB_USER", "detomo_reader")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# New (SQLite)
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_PATH = os.getenv("DB_PATH", "data/chinook.db")
```

### Vanna Connection
```python
# Old (PostgreSQL)
vn.connect_to_postgres(
    host=config.DB_HOST,
    dbname=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    port=config.DB_PORT
)

# New (SQLite)
vn.connect_to_sqlite(config.DB_PATH)
```

### requirements.txt
```txt
# Remove:
psycopg2-binary

# Add (if not already present):
# sqlite3 is built-in, no need to install
```

---

## Table Name Mapping

| PostgreSQL (PRD) | SQLite (Actual) |
|------------------|-----------------|
| Album | albums |
| Artist | artists |
| Customer | customers |
| Employee | employees |
| Genre | genres |
| Invoice | invoices |
| InvoiceLine | invoice_items |
| MediaType | media_types |
| Playlist | playlists |
| PlaylistTrack | playlist_track |
| Track | tracks |

---

## SQL Syntax Differences (if any)

Most SQL queries will work the same, but note:

### Date Functions
```sql
-- PostgreSQL
EXTRACT(YEAR FROM InvoiceDate)
DATE_TRUNC('month', InvoiceDate)

-- SQLite
strftime('%Y', InvoiceDate)
date(InvoiceDate, 'start of month')
```

### Auto Increment
```sql
-- PostgreSQL
SERIAL PRIMARY KEY

-- SQLite
INTEGER PRIMARY KEY AUTOINCREMENT
```

---

## Advantages of SQLite

✅ **Simpler Setup**: No server installation needed
✅ **Portable**: Single file database
✅ **Built-in**: Python sqlite3 module included
✅ **Fast**: Good for development and small-medium datasets
✅ **Zero Configuration**: Works out of the box

---

## Production Considerations

For production deployment, consider:
- SQLite works well for read-heavy workloads
- For high concurrency, PostgreSQL may still be better
- Can migrate to PostgreSQL later if needed
- Vanna AI supports both seamlessly

---

## Next Steps

1. ✅ Update TASK_01 (completed)
2. ⏳ Update TASK_02 with correct table names
3. ⏳ Update TASK_03 with SQLite connection code
4. ⏳ Update TASK_04 with correct queries
5. ⏳ Update CLAUDE.md execution steps
6. ⏳ Update TASK_MASTER.md estimates

---

## Testing Checklist

After updates, verify:
- [ ] All table names use lowercase
- [ ] Connection code uses SQLite
- [ ] No PostgreSQL dependencies in requirements.txt
- [ ] .env template uses DB_PATH
- [ ] Sample queries work with SQLite syntax
- [ ] Training data files use correct table names

---

**Status**: Updates in progress
**Last Updated**: 2025-10-25
