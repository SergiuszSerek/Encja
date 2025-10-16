import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            pages INTEGER,
            author TEXT,
            year INTEGER
        )
    """)
    conn.commit()
    conn.close()