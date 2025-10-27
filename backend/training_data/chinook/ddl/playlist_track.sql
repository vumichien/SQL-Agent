-- Playlist Track Table
-- Junction table linking playlists to tracks (many-to-many relationship)

CREATE TABLE playlist_track (
    PlaylistId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    CONSTRAINT PK_PlaylistTrack PRIMARY KEY (PlaylistId, TrackId),
    FOREIGN KEY (PlaylistId) REFERENCES playlists (PlaylistId)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (TrackId) REFERENCES tracks (TrackId)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
