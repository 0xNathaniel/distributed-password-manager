import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOCAL_PATH = os.path.join(BASE_DIR, "vault.sqlite")

DB_PATH = os.getenv("DB_PATH", DEFAULT_LOCAL_PATH)


def get_db_connection():
    """Helper function to establish SQLite connection."""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize SQLite database and create vault table if it doesn't exist yet."""
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE vault (
                username TEXT PRIMARY KEY,
                server_share TEXT NOT NULL,
                vault_ciphertext BLOB NOT NULL,
                vault_nonce BLOB NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


if __name__ == "__main__":
    init_db()