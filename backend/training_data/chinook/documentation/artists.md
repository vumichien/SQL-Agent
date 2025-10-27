# Artists Table

## Description
Stores information about music artists and bands. Artists can have multiple albums.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| ArtistId | INTEGER | PRIMARY KEY | Unique artist identifier |
| Name | NVARCHAR(120) | | Artist or band name |

## Relationships

**One-to-Many**:
- One Artist → Many Albums

## Business Rules

1. Artist name should be unique (though not enforced by constraint)
2. An artist can have zero or more albums
3. Artist name can be a solo artist or band name

## Common Query Patterns

### List all artists
```sql
SELECT * FROM artists ORDER BY Name;
```

### Artists with album count
```sql
SELECT
    ar.Name,
    COUNT(al.AlbumId) as AlbumCount
FROM artists ar
LEFT JOIN albums al ON ar.ArtistId = al.ArtistId
GROUP BY ar.ArtistId, ar.Name
ORDER BY AlbumCount DESC;
```

### Top artists by sales
```sql
SELECT
    ar.Name as Artist,
    COUNT(il.InvoiceLineId) as TracksSold
FROM artists ar
JOIN albums al ON ar.ArtistId = al.ArtistId
JOIN tracks t ON al.AlbumId = t.AlbumId
JOIN invoice_items il ON t.TrackId = il.TrackId
GROUP BY ar.ArtistId, ar.Name
ORDER BY TracksSold DESC
LIMIT 10;
```

## Japanese Terminology
- アーティスト (aatisuto) = Artist
- バンド (bando) = Band
- ミュージシャン (myuujishan) = Musician
