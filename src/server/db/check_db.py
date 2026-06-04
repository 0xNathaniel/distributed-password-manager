import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "/app/db/vault.sqlite")

def check_vault_contents():
    """Check contents of the vault table in the SQLite database."""

    print(f"Checking database: {DB_PATH}\n")

    if not os.path.exists(DB_PATH):
        print("Database not found. Ensure the server has created the database file or set the DB_PATH environment variable.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        query = f"SELECT username, server_share, vault_ciphertext, vault_nonce FROM vault"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("Database is reachable, but the vault table contains no entries.")
            return

        print(f"Found {len(rows)} vault entries:\n")
        print("=" * 60)

        for row in rows:
            username = row["username"]
            server_share = row["server_share"] or ""

            vault_ct = row["vault_ciphertext"]
            vault_nonce = row["vault_nonce"]

            if vault_ct is None:
                ct_info = "(empty)"
                ct_len = 0
            elif isinstance(vault_ct, str):
                ct_hex = vault_ct
                try:
                    ct_len = len(bytes.fromhex(vault_ct))
                except ValueError:
                    ct_len = len(vault_ct)
                ct_info = f"{ct_hex[:48]}... (length: {ct_len} bytes)"
            else:
                ct_hex = vault_ct.hex()
                ct_len = len(vault_ct)
                ct_info = f"{ct_hex[:48]}... (length: {ct_len} bytes)"

            if vault_nonce is None:
                nonce_info = "(empty)"
            elif isinstance(vault_nonce, str):
                nonce_info = vault_nonce
            else:
                nonce_info = vault_nonce.hex()

            print(f"Username       : {username}")
            print(f"Server share   : {server_share[:40]}{'...' if len(server_share) > 40 else ''}")
            print(f"Ciphertext     : {ct_info}")
            print(f"Nonce          : {nonce_info}")
            print("-" * 60)

    except sqlite3.OperationalError as err:
        print(f"SQLite error: {err}")
        print(f"Check table name: vault and the database structure.")
    finally:
        conn.close()


if __name__ == "__main__":
    check_vault_contents()