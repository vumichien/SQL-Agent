# Tracks Table

## Description
Stores individual music track information including name, duration, composer, and pricing.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| TrackId | INTEGER | PRIMARY KEY | Unique track identifier |
| Name | NVARCHAR(200) | NOT NULL | Track name/title |
| AlbumId | INTEGER | FOREIGN KEY | Reference to Album (optional) |
| MediaTypeId | INTEGER | NOT NULL, FOREIGN KEY | Reference to Media Type |
| GenreId | INTEGER | FOREIGN KEY | Reference to Genre (optional) |
| Composer | NVARCHAR(220) | | Composer name |
| Milliseconds | INTEGER | NOT NULL | Track duration in milliseconds |
| Bytes | INTEGER | | File size in bytes |
| UnitPrice | NUMERIC(10,2) | NOT NULL | Track price |

## Relationships

**Many-to-One**:
- Many Tracks → One Album
- Many Tracks → One Genre
- Many Tracks → One Media Type

**One-to-Many**:
- One Track → Many Invoice Items
- One Track → Many Playlist Track entries

## Business Rules

1. Track name is required
2. Track must have a media type
3. Track may or may not belong to an album
4. Duration (Milliseconds) must be > 0
5. UnitPrice is typically $0.99 or $1.99
6. Composer field is optional

## Common Query Patterns

### Get tracks with album and artist
```sql
SELECT
    t.Name as Track,
    al.Title as Album,
    ar.Name as Artist
FROM tracks t
LEFT JOIN albums al ON t.AlbumId = al.AlbumId
LEFT JOIN artists ar ON al.ArtistId = ar.ArtistId;
```

### Tracks by genre
```sql
SELECT
    g.Name as Genre,
    COUNT(t.TrackId) as TrackCount
FROM tracks t
JOIN genres g ON t.GenreId = g.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY TrackCount DESC;
```

### Longest tracks
```sql
SELECT
    Name,
    ROUND(Milliseconds / 60000.0, 2) as Minutes
FROM tracks
ORDER BY Milliseconds DESC
LIMIT 10;
```

### Tracks with price
```sql
SELECT Name, UnitPrice
FROM tracks
WHERE UnitPrice > 0.99
ORDER BY UnitPrice DESC;
```

## Japanese Terminology
- 曲 (kyoku) = Track/Song
- アルバム (arubamu) = Album
- ジャンル (janru) = Genre
- 作曲家 (sakkyokuka) = Composer
- 再生時間 (saisei jikan) = Duration
- 価格 (kakaku) = Price
