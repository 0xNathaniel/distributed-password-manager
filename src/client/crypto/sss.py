import secrets

from Crypto.Protocol.SecretSharing import Shamir


def generate_master_key() -> bytes:
    # master key random sepanjang 16 byte (128-bit).

    return secrets.token_bytes(16)


def split_key(master_key_bytes: bytes) -> list[str]:
    # split master key into 3 shares with (2, 3) threshold via Shamir GF(2^128)

    shares = Shamir.split(2, 3, master_key_bytes)
    return [f"{idx}-{share.hex()}" for idx, share in shares]


def reconstruct_key(share1: str, share2: str) -> bytes:
    # reconstruct master key from any 2 of the 3 shares

    parsed = []
    for s in (share1, share2):
        idx_str, hex_str = s.split("-", 1)
        parsed.append((int(idx_str), bytes.fromhex(hex_str)))
    return Shamir.combine(parsed)
