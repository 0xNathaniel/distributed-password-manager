import json
import requests
from crypto import aes_gcm, kdf, sss
from cli import storage

SERVER_URL = "http://localhost:8000"


def init_vault(username: str, master_password: str) -> str:
    """Initialize a new vault."""
    master_key = sss.generate_master_key()

    shares = sss.split_key(master_key)
    local_share = shares[0]
    server_share = shares[1]
    recovery_share = shares[2]

    salt = kdf.generate_salt()
    derived_key = kdf.derive_key(master_password, salt)

    local_share_cipher, local_share_nonce = aes_gcm.encrypt_data(
        local_share.encode("utf-8"), derived_key
    )

    storage.save_client_config(salt, local_share_cipher, local_share_nonce)

    empty_vault = json.dumps({}).encode("utf-8")
    vault_cipher, vault_nonce = aes_gcm.encrypt_data(empty_vault, master_key)

    storage.save_backup_vault(vault_cipher, vault_nonce)

    payload = {
        "username": username,
        "server_share": server_share,
        "vault_ciphertext": vault_cipher.hex(),
        "vault_nonce": vault_nonce.hex()
    }

    response = requests.post(f"{SERVER_URL}/api/vault/init", json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to initialize vault: {response.text}")
    
    return recovery_share


def open_vault_normal(username: str, mater_password: str) -> dict:
    """Open vault in normal mode using local share and server share."""
    salt = storage.get_item("kdf_salt")
    local_share_cipher = storage.get_item("local_share_cipher")
    local_share_nonce = storage.get_item("local_share_nonce")

    if not all([salt, local_share_cipher, local_share_nonce]):
        raise Exception("Client not properly initialized. Missing local share data.")
    
    derived_key = kdf.derive_key(mater_password, salt)
    try:
        local_share_bytes = aes_gcm.decrypt_data(local_share_cipher, local_share_nonce, derived_key)
        local_share = local_share_bytes.decode("utf-8")
    except Exception as e:
        raise Exception("Failed to decrypt local share. Incorrect master password?") from e
    
    response = requests.get(f"{SERVER_URL}/api/vault/{username}")
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve vault from server: {response.text}")
    
    server_data = response.json()
    server_share = server_data.get("server_share")
    vault_cipher = bytes.fromhex(server_data.get("vault_ciphertext"))
    vault_nonce = bytes.fromhex(server_data.get("vault_nonce"))

    master_key = sss.reconstruct_key(local_share, server_share)

    try:
        vault_bytes = aes_gcm.decrypt_data(vault_cipher, vault_nonce, master_key)
        vault_data = json.loads(vault_bytes.decode("utf-8"))
        return vault_data
    except Exception as e:
        raise Exception("Failed to decrypt vault. Data may be corrupted.") from e
    

def open_vault_backup(master_password: str, recovery_share: str) -> dict:
    """Open vault in backup mode using recovery share."""
    salt = storage.get_item("kdf_salt")
    local_share_cipher = storage.get_item("local_share_cipher")
    local_share_nonce = storage.get_item("local_share_nonce")

    backup_vault_cipher = storage.get_item("backup_vault_cipher")
    backup_vault_nonce = storage.get_item("backup_vault_nonce")

    if not all([salt, local_share_cipher, local_share_nonce, backup_vault_cipher, backup_vault_nonce]):
        raise Exception("Client not properly initialized. Missing local share or backup vault data.")
    
    derived_key = kdf.derive_key(master_password, salt)
    try:
        local_share_bytes = aes_gcm.decrypt_data(local_share_cipher, local_share_nonce, derived_key)
        local_share = local_share_bytes.decode("utf-8")
    except Exception as e:
        raise Exception("Failed to decrypt local share. Incorrect master password?") from e
    
    try:
        master_key = sss.reconstruct_key(local_share, recovery_share)
    except Exception as e:
        raise Exception("Failed to reconstruct master key. Incorrect recovery share?") from e
    
    try:
        vault_bytes = aes_gcm.decrypt_data(backup_vault_cipher, backup_vault_nonce, master_key)
        vault_data = json.loads(vault_bytes.decode("utf-8"))
        return vault_data
    except Exception as e:
        raise Exception("Failed to decrypt backup vault. Data may be corrupted.") from e