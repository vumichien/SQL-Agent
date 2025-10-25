-- Tracks Table
-- Stores individual music track information

CREATE TABLE tracks (
    TrackId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Name NVARCHAR(200) NOT NULL,
    AlbumId INTEGER,
    MediaTypeId INTEGER NOT NULL,
    GenreId INTEGER,
    Composer NVARCHAR(220),
    Milliseconds INTEGER NOT NULL,
    Bytes INTEGER,
    UnitPrice NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (AlbumId) REFERENCES albums (AlbumId)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (GenreId) REFERENCES genres (GenreId)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (MediaTypeId) REFERENCES media_types (MediaTypeId)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
