import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
            skills TEXT
            )
            ''')

            conn.commit()
            conn.close()