-- Create the temp_transactions table
CREATE TABLE IF NOT EXISTS temp_transactions (
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

-- Create the date table
CREATE TABLE IF NOT EXISTS date (
    id INTEGER PRIMARY KEY,
    original_date TEXT,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    month_name TEXT
);

-- Create the category table
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Create the accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    type TEXT,
    bank TEXT,
    card TEXT
);

-- Create the transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date_id INTEGER,
    description TEXT,
    category_id INTEGER,
    amount REAL,
    account_id INTEGER,
    FOREIGN KEY (date_id) REFERENCES date(id),
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);