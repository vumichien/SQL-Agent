# Playlists Table

## Description
Stores playlist information. Playlists are collections of tracks with many-to-many relationship.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| PlaylistId | INTEGER | PRIMARY KEY | Unique playlist identifier |
| Name | NVARCHAR(120) | | Playlist name |

## Relationships

**Many-to-Many**:
- Many Playlists ↔ Many Tracks (through playlist_track junction table)

## Business Rules

1. Playlist name should be descriptive
2. A playlist can contain zero or more tracks
3. A track can appear in multiple playlists
4. Playlists are curated collections (not user-generated in this model)

## Common Query Patterns

### List all playlists
```sql
SELECT * FROM playlists ORDER BY Name;
```

### Playlists with track count
```sql
SELECT
    p.Name as Playlist,
    COUNT(pt.TrackId) as TrackCount
FROM playlists p
LEFT JOIN playlist_track pt ON p.PlaylistId = pt.PlaylistId
GROUP BY p.PlaylistId, p.Name
ORDER BY TrackCount DESC;
```

### Get tracks in a playlist
```sql
SELECT
    p.Name as Playlist,
    t.Name as Track,
    ar.Name as Artist
FROM playlists p
JOIN playlist_track pt ON p.PlaylistId = pt.PlaylistId
JOIN tracks t ON pt.TrackId = t.TrackId
LEFT JOIN albums al ON t.AlbumId = al.AlbumId
LEFT JOIN artists ar ON al.ArtistId = ar.ArtistId
WHERE p.PlaylistId = 1;
```

## Japanese Terminology
- プレイリスト (purei risuto) = Playlist
- 曲リスト (kyoku risuto) = Song list
