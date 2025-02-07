CREATE TABLE IF NOT EXISTS transactions (
    Year INTEGER,
    Month TEXT,
    Date TEXT,
    Description TEXT,
    Category TEXT,
    Amount REAL,
    Type TEXT,
    Bank TEXT,
    Card TEXT
);

.mode csv

.import cleanNoT.csv transactions

SELECT * FROM transactions;



CREATE TABLE IF NOT EXISTS test (
    Year TEXT,
    id INTEGER
);

insert into test(year, id)
values (2025, 2)

SELECT * FROM test;
