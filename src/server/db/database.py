import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "/app/db/vault.sqlite")

def init_db():
    """Initialize SQLite database and create vault table if it doesn't exist yet."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
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