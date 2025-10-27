-- Albums Table
-- Stores information about music albums

CREATE TABLE albums (
    AlbumId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Title NVARCHAR(160) NOT NULL,
    ArtistId INTEGER NOT NULL,
    FOREIGN KEY (ArtistId) REFERENCES artists (ArtistId)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
