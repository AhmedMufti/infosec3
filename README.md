# Secure Chat System - Assignment #2

## Overview
This is a console-based secure chat system that implements a comprehensive cryptographic protocol to achieve **Confidentiality, Integrity, Authenticity, and Non-Repudiation (CIANR)**.

## Features
- **PKI Setup**: Self-built Certificate Authority (CA) with X.509 certificate generation
- **Mutual Authentication**: Certificate-based authentication between client and server
- **Secure Registration/Login**: MySQL-based user management with salted password hashing
- **Key Agreement**: Diffie-Hellman key exchange for session key establishment
- **Encrypted Messaging**: AES-128 encryption with PKCS#7 padding
- **Message Integrity**: RSA signatures over SHA-256 hashes
- **Non-Repudiation**: Session transcripts and signed receipts

## Repository
**⚠️ Important**: Do NOT fork the skeleton repository. Instead, clone/download it and create your own **private** GitHub repository.

**Deadline**: Monday, 17th Nov, 2025, 11:59 AM (noon)

GitHub: [Your Private Repository URL]

## Prerequisites
- Python 3.8+
- MySQL Server
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd securechat-skeleton
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```bash
mysql -u root -p < database/schema.sql
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

5. Generate CA and certificates:
```bash
python scripts/gen_ca.py
python scripts/gen_cert.py server
python scripts/gen_cert.py client
```

## Execution Steps

### 1. Start the Server
```bash
python server.py
```

### 2. Start the Client
```bash
python client.py
```

### 3. Client Workflow
- The client will connect to the server
- Mutual certificate exchange and validation occurs
- User can register or login
- After authentication, DH key exchange establishes session key
- Encrypted chat messaging begins
- Session ends with transcript and receipt generation

## Configuration

### Server Configuration
- Default port: 9999
- MySQL connection settings in `.env`
- Certificate location: `certs/server_cert.pem`, `certs/server_key.pem`

### Client Configuration
- Server host: `localhost`
- Server port: `9999`
- Certificate location: `certs/client_cert.pem`, `certs/client_key.pem`

## Protocol Phases

1. **Control Plane**: Certificate exchange and authentication
2. **Key Agreement**: Diffie-Hellman key exchange
3. **Data Plane**: Encrypted message exchange
4. **Tear Down**: Session transcript and receipt generation

## Message Formats

### Hello Exchange
```json
{"type": "hello", "client_cert": "...PEM...", "nonce": "base64"}
{"type": "server_hello", "server_cert": "...PEM...", "nonce": "base64"}
```

### Registration
```json
{"type": "register", "email": "...", "username": "...", "pwd": "base64(sha256(salt||pwd))", "salt": "base64"}
```

### Login
```json
{"type": "login", "email": "...", "pwd": "base64(sha256(salt||pwd))", "nonce": "base64"}
```

### Diffie-Hellman Key Exchange
```json
{"type": "dh_client", "g": int, "p": int, "A": int}
{"type": "dh_server", "B": int}
```

### Encrypted Message
```json
{"type": "msg", "seqno": n, "ts": unix_ms, "ct": "base64", "sig": "base64(RSA_SIGN(SHA256(seqno||ts||ct)))"}
```

### Session Receipt
```json
{"type": "receipt", "peer": "client|server", "first_seq": ..., "last_seq": ..., "transcript_sha256": "hex", "sig": "base64"}
```

## Testing

### Certificate Validation Tests
- Invalid certificate rejection
- Expired certificate rejection
- Self-signed certificate rejection

### Security Tests
- Message tampering detection
- Replay attack prevention
- Signature verification

### Evidence Collection
- Wireshark captures showing encrypted payloads
- Transcript verification
- Receipt verification

## Project Structure
```
.
├── scripts/
│   ├── gen_ca.py          # CA generation script
│   └── gen_cert.py        # Certificate generation script
├── certs/                 # Certificates and keys (not committed)
├── transcripts/           # Session transcripts
├── database/
│   └── schema.sql         # MySQL schema
├── server.py              # Server implementation
├── client.py              # Client implementation
├── crypto_utils.py        # Cryptographic utilities
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── README.md             # This file
```

## Security Features

- **Confidentiality**: AES-128 encryption
- **Integrity**: SHA-256 hashing with RSA signatures
- **Authenticity**: X.509 certificate validation
- **Non-Repudiation**: Signed session transcripts and receipts
- **Replay Protection**: Sequence numbers and timestamps
- **Password Security**: Salted SHA-256 hashing

## Notes

- All certificates and keys are stored locally and never committed to GitHub
- Passwords are never transmitted or stored in plaintext
- Session keys are derived fresh for each session
- All messages are signed and encrypted

## Authors
[Your Name] - [Your Roll Number]

## License
This project is for academic purposes only.



