import sqlite3
from pathlib import Path
from app.core.logger import logger

DB_PATH = Path("memory.db")


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def migrate_db():
    logger.info("Starting database migration...")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(conversation_memory)")
        columns = [row["name"] for row in cursor.fetchall()]

        logger.info(f"Existing columns: {columns}")

        cursor.execute("""
            PRAGMA table_info(conversation_memory)
            """)

        columns = [row[1] for row in cursor.fetchall()]

        if "embedding" not in columns:

            logger.info("adding_embedding_column")

            cursor.execute("""
                ALTER TABLE conversation_memory
                ADD COLUMN embedding TEXT
                """)

        if "memory_type" not in columns:
            logger.info("Adding column memory_type")
            cursor.execute("""
                ALTER TABLE conversation_memory
                ADD COLUMN memory_type TEXT
            """)

        if "memory_value" not in columns:
            logger.info("Adding column memory_value")
            cursor.execute("""
                ALTER TABLE conversation_memory
                ADD COLUMN memory_value TEXT
            """)

        conn.commit()

        logger.info("Database migration completed successfully.")

    except Exception as e:
        logger.exception(f"Database migration failed: {e}")
        raise

    finally:
        conn.close()


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
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            memory_type TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    logger.info("user_memory_table_verified")

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_session_id
    ON conversation_memory(session_id)
    """)

    conn.commit()

    conn.close()
