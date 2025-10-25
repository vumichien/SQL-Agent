# Media Types Table

## Description
Stores different media format types such as MP3, AAC, MPEG audio file, etc.

## Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| MediaTypeId | INTEGER | PRIMARY KEY | Unique media type identifier |
| Name | NVARCHAR(120) | | Media type name |

## Relationships

**One-to-Many**:
- One Media Type → Many Tracks

## Business Rules

1. Media type names should be unique
2. Common types: MPEG audio file, AAC audio file, Protected AAC, Protected MPEG-4 video
3. Every track must have a media type

## Common Query Patterns

### List all media types
```sql
SELECT * FROM media_types ORDER BY Name;
```

### Media types with track count
```sql
SELECT
    mt.Name as MediaType,
    COUNT(t.TrackId) as TrackCount
FROM media_types mt
LEFT JOIN tracks t ON mt.MediaTypeId = t.MediaTypeId
GROUP BY mt.MediaTypeId, mt.Name
ORDER BY TrackCount DESC;
```

## Japanese Terminology
- メディアタイプ (media taipu) = Media type
- フォーマット (foomatto) = Format
- 音声ファイル (onsei fairu) = Audio file
