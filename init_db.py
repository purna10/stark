import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'password'))  # Replace with desired credentials
        conn.commit()

if __name__ == "__main__":
    init_db()
