# Secure Chat System - Assignment #2

## Overview
A console-based secure chat system implementing **Confidentiality, Integrity, Authenticity, and Non-Repudiation (CIANR)** using AES-128, RSA, Diffie-Hellman, and X.509 certificates.

**⚠️ Important:** Do NOT fork the skeleton repository. Clone/download it and create your own **private** GitHub repository.

**Deadline:** Monday, 17th Nov, 2025, 11:59 AM (noon)

## Repository
GitHub: [Your Private Repository URL]

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up MySQL Database
```bash
# Option 1: Automated
python setup_database.py

# Option 2: Manual
mysql -u root -p < database/schema.sql
```

### 3. Generate Certificates
```bash
python scripts/gen_ca.py
python scripts/gen_cert.py server
python scripts/gen_cert.py client
```

### 4. Configure Environment
Create `.env` file:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=securechat
SERVER_HOST=localhost
SERVER_PORT=9999
```

### 5. Run the System
```bash
# Terminal 1 - Start Server
python server.py

# Terminal 2 - Start Client
python client.py
```

---

## How to Run Server

```bash
python server.py
```

**Expected Output:**
```
Connected to database: securechat
Server listening on localhost:9999
New connection from ('127.0.0.1', 54321)
Control plane: Certificates exchanged and validated
User registered: alice (alice@example.com)
Key agreement: Session key established
Data plane: Starting encrypted chat
[alice]: Hello, this is a test message
```

---

## How to Run Client

```bash
python client.py
```

**Expected Output:**
```
Connected to server localhost:9999
Control plane: Certificates exchanged and validated

1. Register
2. Login
Enter choice (1/2): 1
Email: alice@example.com
Username: alice
Password: ********
Registration successful!
Key agreement: Session key established

Data plane: Starting encrypted chat
Type messages and press Enter to send
Type 'quit' to end the session

Hello, this is a test message
[Server]: Message 1 received
quit
Session receipt generated: transcripts/client_alice_*.txt
```

---

## MySQL Setup

### Create Database
```sql
CREATE DATABASE securechat;
USE securechat;
```

### Run Schema
```bash
mysql -u root -p < database/schema.sql
```

### Or Use Python Script
```bash
python setup_database.py
```

### Verify Setup
```bash
python test_db.py
```

---

## Sample Input/Output

### Registration Flow
```
Client Input:
  1. Register
  Email: alice@example.com
  Username: alice
  Password: testpass123

Server Output:
  User registered: alice (alice@example.com)
  Key agreement: Session key established

Client Output:
  Registration successful!
  Key agreement: Session key established
```

### Chat Flow
```
Client Input:
  Hello, this is encrypted!
  How are you?
  quit

Server Output:
  [alice]: Hello, this is encrypted!
  [alice]: How are you?

Client Output:
  [Server]: Message 1 received
  [Server]: Message 2 received
  Session receipt generated
```

---

## Testing

### Run All Tests
```bash
python run_all_tests.py
```

### Individual Tests
```bash
# Certificate validation
python test_cert_validation.py

# Database setup
python test_db.py

# Invalid certificate
python test_invalid_cert.py

# Tampering detection
python test_tampering.py

# Replay attack
python test_replay.py

# Non-repudiation
python test_non_repudiation.py
```

See `TESTING_GUIDE.md` for detailed testing instructions.

---

## Project Structure

```
.
├── server.py              # Server implementation
├── client.py              # Client implementation
├── crypto_utils.py        # Cryptographic utilities
├── scripts/
│   ├── gen_ca.py         # CA generation
│   └── gen_cert.py       # Certificate generation
├── database/
│   └── schema.sql        # MySQL schema
├── certs/                # Certificates (not committed)
├── transcripts/          # Session transcripts (not committed)
├── test_*.py             # Test scripts
├── requirements.txt      # Dependencies
├── README.md            # This file
├── FILE_PURPOSE.md      # File purpose explanation
└── TESTING_GUIDE.md     # Testing instructions
```

---

## Assignment Goals Achieved

### ✅ Goal 1: CA and Certificates
- Root CA creation (`scripts/gen_ca.py`)
- Server/client certificate issuance (`scripts/gen_cert.py`)
- Mutual certificate validation
- Invalid certificate rejection

### ✅ Goal 2: Secure Registration & Login
- MySQL database setup
- Encrypted credential transmission
- Salted password hashing: `SHA256(salt || password)`
- Certificate + credential verification

### ✅ Goal 3: Diffie-Hellman Key Exchange
- DH key exchange after login
- Session key derivation: `K = Trunc16(SHA256(Ks))`
- Unique session keys per session

### ✅ Goal 4: Encrypted Chat Messages
- AES-128 encryption with PKCS#7 padding
- Sequence numbers (replay protection)
- Timestamps
- SHA-256 hashing
- RSA digital signatures
- Message verification

### ✅ Goal 5: Non-Repudiation
- Session transcripts
- Transcript hashing
- Signed receipts
- Offline verification

---

## Security Features

- **Confidentiality:** AES-128 encryption
- **Integrity:** SHA-256 + RSA signatures
- **Authenticity:** X.509 certificate validation
- **Non-Repudiation:** Signed session receipts
- **Replay Protection:** Sequence number enforcement

---

## Troubleshooting

### Certificate Errors
- Ensure certificates are generated: `python scripts/gen_ca.py`
- Check certificate files exist in `certs/` directory

### Database Errors
- Verify MySQL is running
- Check database exists: `python test_db.py`
- Verify `.env` file has correct credentials

### Connection Errors
- Check server is running
- Verify port 9999 is available
- Check firewall settings

---

## Documentation

- **FILE_PURPOSE.md** - Explains each file's purpose and assignment goals
- **TESTING_GUIDE.md** - Detailed testing instructions for all required tests
- **README.md** - This file (main documentation)

---

## Submission Checklist

- [ ] GitHub repository (private, ≥10 commits)
- [ ] MySQL schema + sample records
- [ ] README.md (this file)
- [ ] Report: `RollNumber-FullName-Report-A02.docx`
- [ ] Test Report: `RollNumber-FullName-TestReport-A02.docx`
- [ ] Wireshark screenshots
- [ ] All test evidence (invalid cert, tampering, replay, non-repudiation)

---

## Authors
Muhammad Ahmed Mufti - i22-1088

## License
Academic use only.
