-- Foreign Key Relationships in Chinook Database
-- This file documents all relationships between tables

-- Albums -> Artists
-- One artist can have many albums
-- Foreign Key: albums.ArtistId -> artists.ArtistId

-- Customers -> Employees (Support Representative)
-- One employee can support many customers
-- Foreign Key: customers.SupportRepId -> employees.EmployeeId

-- Employees -> Employees (Self-referencing: Manager/Reports To)
-- One employee can manage many employees
-- Foreign Key: employees.ReportsTo -> employees.EmployeeId

-- Invoices -> Customers
-- One customer can have many invoices
-- Foreign Key: invoices.CustomerId -> customers.CustomerId

-- Invoice Items -> Invoices
-- One invoice can have many invoice items (line items)
-- Foreign Key: invoice_items.InvoiceId -> invoices.InvoiceId

-- Invoice Items -> Tracks
-- One track can appear in many invoice items
-- Foreign Key: invoice_items.TrackId -> tracks.TrackId

-- Playlist Track -> Playlists (Many-to-Many Junction)
-- One playlist can have many tracks
-- Foreign Key: playlist_track.PlaylistId -> playlists.PlaylistId

-- Playlist Track -> Tracks (Many-to-Many Junction)
-- One track can be in many playlists
-- Foreign Key: playlist_track.TrackId -> tracks.TrackId

-- Tracks -> Albums
-- One album can have many tracks
-- Foreign Key: tracks.AlbumId -> albums.AlbumId

-- Tracks -> Genres
-- One genre can have many tracks
-- Foreign Key: tracks.GenreId -> genres.GenreId

-- Tracks -> Media Types
-- One media type can have many tracks
-- Foreign Key: tracks.MediaTypeId -> media_types.MediaTypeId

-- Summary of Relationships:
-- 1. artists (1) -> (N) albums
-- 2. albums (1) -> (N) tracks
-- 3. genres (1) -> (N) tracks
-- 4. media_types (1) -> (N) tracks
-- 5. customers (1) -> (N) invoices
-- 6. invoices (1) -> (N) invoice_items
-- 7. tracks (1) -> (N) invoice_items
-- 8. employees (1) -> (N) customers (as support rep)
-- 9. employees (1) -> (N) employees (manager-employee)
-- 10. playlists (N) <-> (N) tracks (through playlist_track)
