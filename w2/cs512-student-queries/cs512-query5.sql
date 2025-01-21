-- List the customer first and last name and address district of all customers from the California district
-- order by their last name descending

SELECT customer.first_name, customer.last_name, address.district
FROM customer
JOIN address ON customer.address_id = address.address_id
WHERE address.district = 'California'
ORDER BY customer.last_name DESC;