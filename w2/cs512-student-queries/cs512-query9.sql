-- Delete all rows from bsg_people where the person has no homeword

DELETE FROM bsg_cert_people
WHERE pid IN (
    SELECT id 
    FROM bsg_people 
    WHERE homeworld IS NULL 
        OR homeworld NOT IN (
            SELECT id 
            FROM bsg_planets
            )
    );

DELETE FROM bsg_ship_assignment
WHERE pid IN (
    SELECT id 
    FROM bsg_people 
    WHERE homeworld IS NULL 
        OR homeworld NOT IN (
            SELECT id 
            FROM bsg_planets
            )
    );

DELETE FROM bsg_people
WHERE homeworld IS NULL
   OR homeworld NOT IN (
    SELECT id 
    FROM bsg_planets
    );