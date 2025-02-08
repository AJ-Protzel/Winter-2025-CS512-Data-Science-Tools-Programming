-- Populate the temp_transactions table
.mode csv
.import --skip 1 "C:/School/Winter-2025-CS512-Data-Science-Tools-Programming/w5/clean.csv" temp_transactions

-- Populate the date table
INSERT INTO date (original_date, year, month, day, month_name)
SELECT DISTINCT 
    Date AS original_date,
    CAST(strftime('%Y', substr(Date, 7, 4) || '-' || substr(Date, 1, 2) || '-' || substr(Date, 4, 2)) AS INTEGER) AS year,
    CAST(strftime('%m', substr(Date, 7, 4) || '-' || substr(Date, 1, 2) || '-' || substr(Date, 4, 2)) AS INTEGER) AS month,
    CAST(strftime('%d', substr(Date, 7, 4) || '-' || substr(Date, 1, 2) || '-' || substr(Date, 4, 2)) AS INTEGER) AS day,
    Month AS month_name
FROM temp_transactions;

-- Populate the category table
INSERT INTO category (name)
SELECT DISTINCT Category FROM temp_transactions;

-- Populate the accounts table
INSERT INTO accounts (type, bank, card)
SELECT DISTINCT Type, Bank, Card FROM temp_transactions;

-- Populate the transactions table
INSERT INTO transactions (date_id, description, category_id, amount, account_id)
SELECT 
    (SELECT id FROM date WHERE original_date = t.Date),
    t.Description,
    (SELECT id FROM category WHERE name = t.Category),
    t.Amount,
    (SELECT id FROM accounts WHERE type = t.Type AND bank = t.Bank AND card = t.Card)
FROM temp_transactions t;