-- Media Types Table
-- Stores different media format types (MP3, AAC, etc.)

CREATE TABLE media_types (
    MediaTypeId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Name NVARCHAR(120)
);
