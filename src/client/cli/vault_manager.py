import json
import requests
from crypto import aes_gcm, kdf, sss
from cli import storage

SERVER_URL = "http://localhost:8000"


def init_vault(username: str, master_password: str) -> str:

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