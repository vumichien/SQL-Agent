# Genres Table

## Description
Stores music genre classifications such as Rock, Jazz, Classical, etc.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| GenreId | INTEGER | PRIMARY KEY | Unique genre identifier |
| Name | NVARCHAR(120) | | Genre name |

## Relationships

**One-to-Many**:
- One Genre → Many Tracks

## Business Rules

1. Genre names should be unique
2. A genre can have zero or more tracks
3. Common genres include: Rock, Jazz, Metal, Classical, Blues, etc.

## Common Query Patterns

### List all genres
```sql
SELECT * FROM genres ORDER BY Name;
```

### Genres with track count
```sql
SELECT
    g.Name as Genre,
    COUNT(t.TrackId) as TrackCount
FROM genres g
LEFT JOIN tracks t ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY TrackCount DESC;
```

### Most popular genre by sales
```sql
SELECT
    g.Name as Genre,
    SUM(il.Quantity) as TotalSold
FROM genres g
JOIN tracks t ON g.GenreId = t.GenreId
JOIN invoice_items il ON t.TrackId = il.TrackId
GROUP BY g.GenreId, g.Name
ORDER BY TotalSold DESC;
```

## Japanese Terminology
- ジャンル (janru) = Genre
- 音楽ジャンル (ongaku janru) = Music genre
- ロック (rokku) = Rock
- ジャズ (jazu) = Jazz
- クラシック (kurashikku) = Classical
