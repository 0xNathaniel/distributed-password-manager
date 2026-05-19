# File: server/api/schemas.py
from pydantic import BaseModel

class VaultInitRequest(BaseModel):
    username: str
    server_share: str
    vault_ciphertext: str  
    vault_nonce: str       

class VaultUpdateRequest(BaseModel):
    vault_ciphertext: str
    vault_nonce: str

class VaultResponse(BaseModel):
    username: str
    server_share: str
    vault_ciphertext: str
    vault_nonce: str