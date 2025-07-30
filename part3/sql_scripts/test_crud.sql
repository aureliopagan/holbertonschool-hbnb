-- testing CRUD operations
USE hbnb_db;

-- Create
INSERT INTO users (first_name, last_name, email, password)
VALUES (
    'John',
    'Doe',
    'john.doe@example.com',
    '$2y$10$O.kKJw3fvaiHNfy3rpkGC.vFU//6G7DRKJNjp/Ql3bltbItQoV3TS' -- 'John_s_password01'
);

-- Read
SELECT * FROM users;

SELECT * FROM amenities;

-- Update
UPDATE users
SET first_name = 'Johnny'
WHERE email = 'john.doe@example.com';

-- Delete
DELETE FROM amenities
WHERE name = 'Swimming Pool';


-- Verify all changes
SELECT * FROM users;

SELECT * FROM amenities;