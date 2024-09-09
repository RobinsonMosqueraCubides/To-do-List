import sqlite3

def setup_database():
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
