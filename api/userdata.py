import sqlite3

def init_db():
    conn = sqlite3.connect('preferences.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS UserPreferences (
            id INTEGER PRIMARY KEY,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
