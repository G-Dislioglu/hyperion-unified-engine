import sqlite3

DB="hue.db"

def conn(): 
    return sqlite3.connect(DB, isolation_level=None)

def init_db():
    c=conn().cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        module TEXT,
        payload TEXT,
        result TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("CREATE TABLE IF NOT EXISTS users(api_key TEXT PRIMARY KEY)")
    conn().commit()

def valid_api_key(key):
    return conn().execute("SELECT 1 FROM users WHERE api_key=?", (key,)).fetchone() is not None
