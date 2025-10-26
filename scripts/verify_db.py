import sqlite3
import sys
import io

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_database():
    print("Verifying Chinook Database...")

    # Connect to database
    conn = sqlite3.connect('data/chinook.db')
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\n[OK] Found {len(tables)} tables:")

    # Count rows in each table
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  - {table}: {count:,} rows")

    # Test sample queries
    print("\nTesting sample queries:")

    # Query 1: Total customers
    cursor.execute("SELECT COUNT(*) FROM customers")
    print(f"  [OK] Total customers: {cursor.fetchone()[0]}")

    # Query 2: Total revenue
    cursor.execute("SELECT SUM(Total) FROM invoices")
    revenue = cursor.fetchone()[0]
    print(f"  [OK] Total revenue: ${revenue:,.2f}")

    # Query 3: Top artist
    cursor.execute("""
        SELECT ar.Name, COUNT(al.AlbumId) as albums
        FROM artists ar
        JOIN albums al ON ar.ArtistId = al.ArtistId
        GROUP BY ar.ArtistId
        ORDER BY albums DESC
        LIMIT 1
    """)
    top_artist = cursor.fetchone()
    print(f"  [OK] Top artist: {top_artist[0]} ({top_artist[1]} albums)")

    conn.close()
    print("\n[SUCCESS] Database verification completed successfully!")
    return True

if __name__ == "__main__":
    verify_database()
