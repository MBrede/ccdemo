-- Runs once, when PostgreSQL initialises an empty data volume.
CREATE TABLE recipe (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    cuisine VARCHAR NOT NULL,
    preparation_time INTEGER NOT NULL,
    is_vegetarian BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO recipe (name, cuisine, preparation_time, is_vegetarian) VALUES
    ('Margherita Pizza', 'Italian', 30, TRUE),
    ('Ramen', 'Japanese', 45, FALSE),
    ('Ratatouille', 'French', 60, TRUE),
    ('Tacos al Pastor', 'Mexican', 40, FALSE);
