-- Create admin table
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_url TEXT UNIQUE NOT NULL,
    last_latitude REAL,
    last_longitude REAL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
