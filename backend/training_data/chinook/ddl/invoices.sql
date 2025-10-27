-- Invoices Table
-- Stores customer order/purchase information

CREATE TABLE invoices (
    InvoiceId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    CustomerId INTEGER NOT NULL,
    InvoiceDate DATETIME NOT NULL,
    BillingAddress NVARCHAR(70),
    BillingCity NVARCHAR(40),
    BillingState NVARCHAR(40),
    BillingCountry NVARCHAR(40),
    BillingPostalCode NVARCHAR(10),
    Total NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES customers (CustomerId)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);
