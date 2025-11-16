# File Purpose and Assignment Goals

This document explains how each file contributes to achieving the assignment goals.

## Assignment Goals Overview

1. **CA and Certificates** - Create root CA and issue certificates
2. **Secure Registration & Login** - MySQL database with encrypted credentials
3. **Diffie-Hellman Key Exchange** - Session key establishment
4. **Encrypted Chat Messages** - AES-128 encryption with RSA signatures
5. **Non-Repudiation** - Session transcripts and receipts

---

## Core Implementation Files

### `server.py`
**Purpose:** Main server implementation  
**Assignment Goals Achieved:**
- ✅ Certificate validation (Goal 1)
- ✅ Secure registration/login with MySQL (Goal 2)
- ✅ Diffie-Hellman key exchange (Goal 3)
- ✅ Encrypted message handling (Goal 4)
- ✅ Session transcript and receipt generation (Goal 5)

**How to Run:**
```bash
python server.py
```

**What it does:**
- Listens on port 9999
- Validates client certificates
- Handles user registration/login
- Performs DH key exchange
- Receives and verifies encrypted messages
- Generates session transcripts and receipts

---

### `client.py`
**Purpose:** Main client implementation  
**Assignment Goals Achieved:**
- ✅ Certificate exchange and validation (Goal 1)
- ✅ Secure registration/login (Goal 2)
- ✅ Diffie-Hellman key exchange (Goal 3)
- ✅ Encrypted message sending (Goal 4)
- ✅ Session transcript and receipt generation (Goal 5)

**How to Run:**
```bash
python client.py
```

**What it does:**
- Connects to server
- Exchanges certificates
- Registers/logs in users
- Performs DH key exchange
- Sends encrypted and signed messages
- Generates session transcripts and receipts

---

### `crypto_utils.py`
**Purpose:** Cryptographic utility functions  
**Assignment Goals Achieved:**
- ✅ Certificate validation (Goal 1)
- ✅ Password hashing with salt (Goal 2)
- ✅ Diffie-Hellman key derivation (Goal 3)
- ✅ AES-128 encryption/decryption (Goal 4)
- ✅ RSA signatures (Goal 4)
- ✅ Transcript hashing (Goal 5)

**Key Functions:**
- `validate_certificate()` - Validates X.509 certificates
- `derive_session_key()` - Derives AES key from DH secret
- `aes_encrypt()` / `aes_decrypt()` - AES-128 encryption
- `rsa_sign()` / `rsa_verify()` - RSA signatures
- `compute_transcript_hash()` - Transcript hashing

---

## Certificate Generation Scripts

### `scripts/gen_ca.py`
**Purpose:** Generate root Certificate Authority  
**Assignment Goal:** Goal 1 - Make Your Own CA

**How to Run:**
```bash
python scripts/gen_ca.py
```

**What it does:**
- Generates CA private key (2048-bit RSA)
- Creates self-signed CA certificate
- Saves to `certs/ca_key.pem` and `certs/ca_cert.pem`
- Valid for 10 years (configurable)

**Output:**
- CA certificate and private key
- Certificate information display

---

### `scripts/gen_cert.py`
**Purpose:** Issue certificates for server and client  
**Assignment Goal:** Goal 1 - Issue Client and Server Certificates

**How to Run:**
```bash
python scripts/gen_cert.py server
python scripts/gen_cert.py client
```

**What it does:**
- Generates RSA keypair for entity
- Creates X.509 certificate signed by CA
- Saves certificate and key to `certs/` directory
- Includes proper extensions (KeyUsage, ExtendedKeyUsage)

**Output:**
- Server/client certificate and private key
- Certificate information display

---

## Database Files

### `database/schema.sql`
**Purpose:** MySQL database schema  
**Assignment Goal:** Goal 2 - Setup MySQL Database

**How to Run:**
```bash
mysql -u root -p < database/schema.sql
```

**What it does:**
- Creates `securechat` database
- Creates `users` table with:
  - `email` (unique)
  - `username` (unique)
  - `salt` (16 bytes binary)
  - `pwd_hash` (64-char hex SHA-256 hash)

**Assignment Requirement:**
- Stores `SHA256(salt || password)` as required

---

### `setup_database.py`
**Purpose:** Automated database table creation  
**Assignment Goal:** Goal 2 - Database Setup Helper

**How to Run:**
```bash
python setup_database.py
```

**What it does:**
- Connects to MySQL database
- Creates `users` table if it doesn't exist
- Verifies table structure

---

## Configuration Files

### `requirements.txt`
**Purpose:** Python dependencies  
**Required for:** All goals

**Contents:**
- `cryptography` - For certificates, encryption, signatures
- `pymysql` - For MySQL database connection
- `python-dotenv` - For environment variable management

**How to Use:**
```bash
pip install -r requirements.txt
```

---

### `.gitignore`
**Purpose:** Prevent committing sensitive files  
**Required for:** Security best practices

**What it excludes:**
- Certificate files (`certs/*.pem`, `certs/*.key`)
- Environment files (`.env`)
- Transcripts
- Database files

---

## Test Files

### `test_cert_validation.py`
**Purpose:** Test certificate validation  
**Assignment Goal:** Goal 1 - Certificate Validation Testing

**How to Run:**
```bash
python test_cert_validation.py
```

**What it tests:**
- Certificate loading
- Certificate validation against CA
- Verifies validation works correctly

---

### `test_db.py`
**Purpose:** Test database connection and setup  
**Assignment Goal:** Goal 2 - Database Verification

**How to Run:**
```bash
python test_db.py
```

**What it tests:**
- Database connection
- Table existence
- Table structure verification

---

### `test_invalid_cert.py`
**Purpose:** Test invalid certificate rejection  
**Assignment Goal:** Goal 1 - Invalid Certificate Test

**How to Run:**
```bash
python test_invalid_cert.py
```

**What it tests:**
- Creates a self-signed certificate
- Demonstrates how invalid certs are rejected
- Shows "BAD CERT" error message

**Evidence for Report:**
- Shows server rejects invalid certificates

---

### `test_tampering.py`
**Purpose:** Test message tampering detection  
**Assignment Goal:** Goal 4 - Tampering Test

**How to Run:**
```bash
python test_tampering.py
```

**What it tests:**
- Simulates message tampering
- Shows signature verification failure
- Demonstrates "SIG FAIL" detection

**Evidence for Report:**
- Shows tampered messages are rejected

---

### `test_replay.py`
**Purpose:** Test replay attack prevention  
**Assignment Goal:** Goal 4 - Replay Test

**How to Run:**
```bash
python test_replay.py
```

**What it tests:**
- Sequence number enforcement
- Replay attack simulation
- Shows "REPLAY" error message

**Evidence for Report:**
- Shows replayed messages are rejected

---

### `test_non_repudiation.py`
**Purpose:** Test non-repudiation verification  
**Assignment Goal:** Goal 5 - Non-Repudiation Test

**How to Run:**
```bash
python test_non_repudiation.py
```

**What it tests:**
- Transcript hash computation
- Receipt verification
- Tampering detection in transcripts

**Evidence for Report:**
- Shows transcript modification breaks signature

---

### `run_all_tests.py`
**Purpose:** Run all tests automatically  
**Assignment Goal:** Comprehensive Testing

**How to Run:**
```bash
python run_all_tests.py
```

**What it does:**
- Runs all test scripts
- Shows summary of results
- Verifies all features work

---

## Documentation Files

### `README.md`
**Purpose:** Main documentation  
**Assignment Requirement:** Must be submitted

**Contents:**
- How to run server
- How to run client
- MySQL setup instructions
- Sample input/output
- GitHub repo link

---

### `FILE_PURPOSE.md` (This File)
**Purpose:** Explain each file's purpose and assignment goals

---

## Setup Scripts

### `setup.sh` / `setup.bat`
**Purpose:** Automated setup script  
**Platform:** Linux/Mac (`.sh`) or Windows (`.bat`)

**How to Run:**
```bash
# Linux/Mac
bash setup.sh

# Windows
setup.bat
```

**What it does:**
- Installs dependencies
- Sets up database
- Generates certificates

---

## Directory Structure

### `certs/`
**Purpose:** Store certificates and keys  
**Assignment Goal:** Goal 1

**Contents:**
- `ca_cert.pem` - CA certificate
- `ca_key.pem` - CA private key
- `server_cert.pem` - Server certificate
- `server_key.pem` - Server private key
- `client_cert.pem` - Client certificate
- `client_key.pem` - Client private key

**Note:** Never commit these files (in `.gitignore`)

---

### `transcripts/`
**Purpose:** Store session transcripts  
**Assignment Goal:** Goal 5

**Contents:**
- Session transcript files
- Contains message history and receipts

**Note:** Never commit these files (in `.gitignore`)

---

### `database/`
**Purpose:** Database schema and setup  
**Assignment Goal:** Goal 2

**Contents:**
- `schema.sql` - MySQL schema definition

---

## How Each File Achieves Assignment Goals

### Goal 1: CA and Certificates
- ✅ `scripts/gen_ca.py` - Creates root CA
- ✅ `scripts/gen_cert.py` - Issues certificates
- ✅ `crypto_utils.py` - Validates certificates
- ✅ `server.py` / `client.py` - Exchange and validate certificates
- ✅ `test_invalid_cert.py` - Tests invalid cert rejection

### Goal 2: Secure Registration & Login
- ✅ `database/schema.sql` - MySQL schema
- ✅ `setup_database.py` - Database setup
- ✅ `server.py` - Registration/login logic
- ✅ `client.py` - Registration/login interface
- ✅ `crypto_utils.py` - Password hashing

### Goal 3: Diffie-Hellman Key Exchange
- ✅ `server.py` - Server-side DH implementation
- ✅ `client.py` - Client-side DH implementation
- ✅ `crypto_utils.py` - Key derivation function

### Goal 4: Encrypted Chat Messages
- ✅ `crypto_utils.py` - AES encryption, RSA signatures
- ✅ `server.py` - Message verification and decryption
- ✅ `client.py` - Message encryption and signing
- ✅ `test_tampering.py` - Tampering detection test
- ✅ `test_replay.py` - Replay attack test

### Goal 5: Non-Repudiation
- ✅ `server.py` - Transcript and receipt generation
- ✅ `client.py` - Transcript and receipt generation
- ✅ `crypto_utils.py` - Transcript hashing
- ✅ `test_non_repudiation.py` - Receipt verification test

---

## Quick Start Guide

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database:**
   ```bash
   python setup_database.py
   ```

3. **Generate certificates:**
   ```bash
   python scripts/gen_ca.py
   python scripts/gen_cert.py server
   python scripts/gen_cert.py client
   ```

4. **Run tests:**
   ```bash
   python run_all_tests.py
   ```

5. **Start system:**
   ```bash
   # Terminal 1
   python server.py
   
   # Terminal 2
   python client.py
   ```

---

## Summary

All assignment goals are achieved through the combination of:
- **Core files** (`server.py`, `client.py`, `crypto_utils.py`) - Main implementation
- **Certificate scripts** (`scripts/gen_*.py`) - PKI setup
- **Database files** (`database/schema.sql`, `setup_database.py`) - User storage
- **Test files** (`test_*.py`) - Verification and evidence
- **Documentation** (`README.md`, `FILE_PURPOSE.md`) - Instructions and explanation

The system is complete and ready for submission! 🎉

