-- populate the tables with initial data
USE hbnb_db;

INSERT INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2y$10$WyIGHzX2TCHKI1q.bgBy.utbKuHaBkQ0wfIUu9mgKkgDDxE.NH9DW',
    True
    );

INSERT INTO amenities (name)
VALUES ('WiFi'), ('Swimming Pool'), ('Air Conditioning');