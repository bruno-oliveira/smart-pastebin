import sqlite3


def create_schema():
    conn = sqlite3.connect("snippets.db")
    cursor = conn.cursor()

# Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS snippets (
                        id INTEGER PRIMARY KEY,
                        snippet_id TEXT UNIQUE,
                        snippet TEXT,
                        explanation TEXT
                    )''')

    cursor.close()
    print("Created")
