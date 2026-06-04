# File: server/api/routes.py
from fastapi import APIRouter, HTTPException
from api.schemas import VaultInitRequest, VaultUpdateRequest, VaultResponse
from db.database import get_db_connection

vault_router = APIRouter(
    prefix="/api/vault", 
    tags=["Vault"]
)

@vault_router.post("/init", response_model=dict)
def init_vault(request: VaultInitRequest):
    """Save new vault data."""
    print("\n[SERVER LOG] INCOMING INITIALIZATION PAYLOAD ", flush=True)
    print(f"  Username    : {request.username}", flush=True)
    print(f"  Server Share: {request.server_share[:40]}...", flush=True)
    print(f"  Ciphertext  : {request.vault_ciphertext[:40]}... (length: {len(request.vault_ciphertext)} hex chars)", flush=True)
    print(f"  Nonce       : {request.vault_nonce}", flush=True)
    print("---------------------------------------------------\n", flush=True)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT username FROM vault WHERE username = ?", 
            (request.username,)
        )
        
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Vault for this user already exists.")
        
        cursor.execute(
            "INSERT INTO vault (username, server_share, vault_ciphertext, vault_nonce) VALUES (?, ?, ?, ?)",
            (request.username, request.server_share, request.vault_ciphertext, request.vault_nonce)
        )
        conn.commit()
        return {"message": "Vault successfully created."}
    finally:
        conn.close()


@vault_router.get("/{username}", response_model=VaultResponse)
def get_vault(username: str):
    """Send server share, encrypted vault, and nonce back to client (Normal Mode)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT username, server_share, vault_ciphertext, vault_nonce FROM vault WHERE username = ?", 
            (username,)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Vault not found.")
            
        return VaultResponse(**dict(row))
    finally:
        conn.close()


@vault_router.put("/{username}", response_model=dict)
def update_vault(username: str, request: VaultUpdateRequest):
    """Receive updated encrypted vault from client after password addition/modification."""
    print("\n[SERVER LOG] INCOMING UPDATE PAYLOAD", flush=True)
    print(f"  Username  : {username}", flush=True)
    print(f"  Ciphertext: {request.vault_ciphertext[:40]}... (length: {len(request.vault_ciphertext)} hex chars)", flush=True)
    print(f"  Nonce     : {request.vault_nonce}", flush=True)
    print("-------------------------------------------\n", flush=True)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "SELECT username FROM vault WHERE username = ?", 
            (username,)
        )
        
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vault not found.")
        
        cursor.execute(
            "UPDATE vault SET vault_ciphertext = ?, vault_nonce = ? WHERE username = ?",
            (request.vault_ciphertext, request.vault_nonce, username)
        )
        conn.commit()
        return {"message": "Vault successfully updated."}
    finally:
        conn.close()