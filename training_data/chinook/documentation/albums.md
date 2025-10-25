# Albums Table

## Description
Stores music album information. Each album belongs to one artist and contains multiple tracks.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| AlbumId | INTEGER | PRIMARY KEY | Unique album identifier |
| Title | NVARCHAR(160) | NOT NULL | Album title |
| ArtistId | INTEGER | NOT NULL, FOREIGN KEY | Reference to Artist |

## Relationships

**Many-to-One**:
- Many Albums → One Artist

**One-to-Many**:
- One Album → Many Tracks

## Business Rules

1. Album title is required
2. Every album must belong to an artist
3. An album can have zero or more tracks
4. Album titles are not necessarily unique (different artists can have same album title)

## Common Query Patterns

### List albums with artist names
```sql
SELECT
    al.Title as Album,
    ar.Name as Artist
FROM albums al
JOIN artists ar ON al.ArtistId = ar.ArtistId
ORDER BY ar.Name, al.Title;
```

### Count albums per artist
```sql
SELECT
    ar.Name as Artist,
    COUNT(al.AlbumId) as AlbumCount
FROM artists ar
LEFT JOIN albums al ON ar.ArtistId = al.ArtistId
GROUP BY ar.ArtistId, ar.Name
ORDER BY AlbumCount DESC;
```

### Albums with track count
```sql
SELECT
    al.Title,
    COUNT(t.TrackId) as TrackCount
FROM albums al
LEFT JOIN tracks t ON al.AlbumId = t.AlbumId
GROUP BY al.AlbumId, al.Title
ORDER BY TrackCount DESC;
```

## Japanese Terminology
- アルバム (arubamu) = Album
- アーティスト (aatisuto) = Artist
- タイトル (taitoru) = Title
- トラック数 (torakku suu) = Track count
