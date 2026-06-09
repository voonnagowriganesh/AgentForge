import sqlite3
from pathlib import Path

DB_PATH = Path("memory.db")


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_memory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id TEXT NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_session_id
    ON conversation_memory(session_id)
    """)

    conn.commit()

    conn.close()
