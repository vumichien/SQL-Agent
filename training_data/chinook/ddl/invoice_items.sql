-- Invoice Items Table
-- Stores line items for each invoice (purchased tracks)

CREATE TABLE invoice_items (
    InvoiceLineId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    InvoiceId INTEGER NOT NULL,
    TrackId INTEGER NOT NULL,
    UnitPrice NUMERIC(10,2) NOT NULL,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (InvoiceId) REFERENCES invoices (InvoiceId)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    FOREIGN KEY (TrackId) REFERENCES tracks (TrackId)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
