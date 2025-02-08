-- Delete records with the 'transfer' category from the transactions table
DELETE FROM transactions
WHERE category_id = (SELECT id FROM category WHERE name = 'transfer');

-- Delete the 'transfer' category from the category table
DELETE FROM category
WHERE name = 'transfer';