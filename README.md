# Distributed Password Manager

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?logo=uvicorn&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![cryptography](https://img.shields.io/badge/cryptography-AES%20GCM-3C5280?logo=letsencrypt&logoColor=white)
![PyCryptodome](https://img.shields.io/badge/PyCryptodome-Shamir%20SSS-006400)
![Requests](https://img.shields.io/badge/Requests-2CA5E0?logo=python&logoColor=white)
![qrcode](https://img.shields.io/badge/qrcode-555555)
![Pillow](https://img.shields.io/badge/Pillow-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)

## Description

A command line distributed password manager built for Tugas 4 II4021 Kriptografi at Institut Teknologi Bandung. It stores account data inside an encrypted vault, where each entry holds a service name, a username or email, a password, and an optional note. The whole vault is encrypted with AES-128-GCM.

The master key that opens the vault is never stored as a whole. It is split with Shamir Secret Sharing using a (2, 3) threshold into three shares: a local share kept on the client, a server share kept on the server, and a recovery share given to the user. Any two valid shares can rebuild the master key.

The program supports two access modes. Normal mode combines the local share with the server share, reads the vault from the server, and writes changes back to it. Backup mode combines the local share with the recovery share, reads from a local encrypted backup, and is read only for emergencies when the server is unreachable. Because the server only ever holds ciphertext and a single share, compromising the server alone is not enough to open a vault.

As a bonus, the recovery share is also rendered as a QR code and split into two image shares with a (2, 2) visual cryptography scheme, so that stacking both images reproduces a scannable QR code.

## Tech Stack

| Category | Technology | Purpose |
| - | - | - |
| Language | Python 3.12 | The whole project |
| Client cryptography | cryptography | AES-128-GCM and PBKDF2-HMAC-SHA256 |
| Client cryptography | PyCryptodome | Shamir Secret Sharing over GF(2^128) |
| Client cryptography | secrets (standard library) | CSPRNG for the master key and generated passwords |
| Visual cryptography | qrcode, Pillow | Render the recovery share and split it into image shares |
| Client networking | requests | Talk to the server over HTTP |
| Server | FastAPI, Uvicorn | The HTTP API and the server that runs it |
| Server | Pydantic | Request and response validation |
| Server | SQLite | Storage for ciphertext and shares |
| Tooling | Docker, Docker Compose | Run the server in a container |
| Tooling | pytest | The cryptography test suite |

## Dependencies

Python 3.12 or newer is required. The exact install commands are listed in the next section.

| Package | Scope | Purpose |
| - | - | - |
| cryptography | Client | AES-128-GCM and the KDF |
| pycryptodome | Client | Shamir Secret Sharing |
| requests | Client | HTTP calls to the server |
| qrcode | Client | QR generation for the recovery share |
| Pillow | Client | Image handling for the visual shares |
| fastapi | Server | The web framework |
| uvicorn | Server | The ASGI server that runs it |
| pydantic | Server | Schema validation |
| python-dotenv | Server | Loading environment variables |
| pytest | Development | Running the cryptography tests |

Client packages are listed in src/client/requirements.txt, server packages in src/server/requirements.txt, and the development setup in requirements-dev.txt.

## How to Run

Create and activate a virtual environment. On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the client and server dependencies:

```powershell
pip install -r src/client/requirements.txt
pip install -r src/server/requirements.txt
```

Start the server. Option A runs it locally with Uvicorn:

```powershell
uvicorn main:app --app-dir src/server --reload --port 8000
```

Option B runs it in Docker:

```powershell
docker compose up --build
```

Check that the server is alive:

```powershell
curl http://localhost:8000/
```

In a second terminal, start the client:

```powershell
python src/client/main.py
```

The client expects the server to be reachable at localhost on port 8000.

## Environment and Configuration

DB_PATH (server)

- Selects where the server keeps its SQLite database.
- Defaults to src/server/db/vault.sqlite locally, and to /app/db/vault.sqlite in Docker.
- To point a local inspection script at the same database the local server uses, set it first:

```powershell
$env:DB_PATH="src/server/db/vault.sqlite"
```

PYTHONUNBUFFERED (server)

- Set to 1 by Docker Compose so the server logs stream live instead of being buffered.

client_data.json (client)

- Created in the directory you run the client from.
- Holds the KDF salt, the encrypted local share with its nonce, and the encrypted backup vault with its nonce.

Server address (client)

- Fixed to localhost on port 8000 in the client source.
- Run the server on that address, or adjust the source if you need a different host.

Recovery share

- Shown only once when the vault is created.
- Keeping it safe is the responsibility of the user.

## Authors

| NIM | Name |
| - | - |
| 13523013 | Nathaniel Jonathan Rusli |
| 13523015 | Maheswara Bayu Kaindra |
| 13523039 | Peter Wongsoredjo |
