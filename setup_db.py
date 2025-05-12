import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table with new columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birthday DATE NOT NULL
    )
''')

# Insert sample admin user (plain password for vulnerable demo)
cursor.execute("INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, birthday) VALUES ('admin', '0xkillua', 'admin@example.com', 'Elsayed', 'Osama', '2004-01-15')")

conn.commit()
conn.close()

print("✅ Database setup complete.")