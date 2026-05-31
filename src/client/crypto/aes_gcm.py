import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LENGTH = 12


class DecryptionError(ValueError):
    """thrown when decryption with AES-GCM fails (MAC validation fails)"""


def encrypt_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    # encrypt data with AES-128-GCM and 12-byte random nonce
    
    nonce = secrets.token_bytes(NONCE_LENGTH)
    ciphertext = AESGCM(key).encrypt(nonce, data, None)
    return ciphertext, nonce


def decrypt_data(ciphertext: bytes, nonce: bytes, key: bytes) -> bytes:
    # decrypt data with AES-128-GCM and 12-byte random nonce
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag as exc:
        raise DecryptionError("Otentikasi AES-GCM gagal: data korup atau kunci salah.") from exc
