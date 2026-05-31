import secrets

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

KDF_ITERATIONS = 600_000 # OWASP 2023
KEY_LENGTH = 16
SALT_LENGTH = 16


def generate_salt() -> bytes:
    # 16 byte salt for KDF

    return secrets.token_bytes(SALT_LENGTH)


def derive_key(password: str, salt: bytes) -> bytes:
    # derive AES-128 key from master password and salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))
