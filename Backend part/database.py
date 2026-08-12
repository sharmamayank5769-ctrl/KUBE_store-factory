import sqlite3

def get_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id TEXT NOT NULL,
        user_id INTEGER,
        status TEXT DEFAULT 'provisioning',
        storage TEXT DEFAULT '2Gi',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    con.commit()
    con.close()
    print("Database ready!")

if __name__ == '__main__':
    init_db()