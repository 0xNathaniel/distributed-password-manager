import json
import os

STORAGE_FILE = "client_data.json"


def load_data() -> dict:
    """Load client data from storage file."""
    if not os.path.exists(STORAGE_FILE):
        return {}
    
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading data: {e}")
        return {}
    

def save_data(data: dict) -> None:
    """Save client data to storage file."""
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    except IOError as e:
        print(f"Error saving data: {e}")


def save_client_config(kdf_salt: bytes, local_share_cipher: bytes, local_share_nonce: bytes) -> None:
    """Save KDF salt and local share encryption details to storage."""
    data = load_data()
    data["kdf_salt"] = kdf_salt.hex()
    data["local_share_cipher"] = local_share_cipher.hex()
    data["local_share_nonce"] = local_share_nonce.hex()
    save_data(data)


def save_backup_vault(backup_vault_cipher: bytes, backup_vault_nonce: bytes) -> None:
    """Save backup vault encryption details to storage."""
    data = load_data()
    data["backup_vault_cipher"] = backup_vault_cipher.hex()
    data["backup_vault_nonce"] = backup_vault_nonce.hex()
    save_data(data)


def get_item(key: str) -> bytes:
    """Retrieve a specific item from storage by key."""
    data = load_data()
    val = data.get(key)

    if val is not None:
        return bytes.fromhex(val)
    return None


def is_initialized() -> bool:
    """Check if the client is initialized with all required keys."""
    data = load_data()
    required_keys = ["kdf_salt", "local_share_cipher", "local_share_nonce"]
    return all(key in data for key in required_keys)



