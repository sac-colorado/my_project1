CREATE TABLE book_info (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);


