import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert sample admin user
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '0xkillua')")

# Save changes and close connection
conn.commit()
conn.close()

print ("Database setup complete.")