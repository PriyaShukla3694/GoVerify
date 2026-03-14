import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'db.sqlite')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            inferred_literacy_level TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS form_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            district TEXT,
            tehsil TEXT,
            village TEXT,
            form_mode_used TEXT,
            is_synced BOOLEAN DEFAULT 1,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES users(session_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS locations_dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_type TEXT NOT NULL,
            name TEXT NOT NULL,
            parent_id INTEGER NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS behavior_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            typing_speed FLOAT,
            error_rate FLOAT,
            pause_time FLOAT,
            classified_as TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
