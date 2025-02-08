downloaded windows x64 tools from https://www.sqlite.org/download.html
put sqlite3.exe into folder on c, added to PATH
installed vscode sqlite3 extention


CREATE TABLE temp_transactions (
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

<in SQLite cmd> <give some time between commands for system to catch up>
.cd C:\School\Winter-2025-CS512-Data-Science-Tools-Programming\w5
.system dir
.open transactions.db
.mode csv
.import --skip 1 "clean.csv" temp_transactions

<back in VSCode>
SELECT * FROM transactions;


.\run_all.bat
