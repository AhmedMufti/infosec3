# Assignment #2 - Secure Chat System

## ✅ Completed Requirements

### 1. CA and Certificates ✅
- **Root CA Created**: `scripts/gen_ca.py` generates root CA
- **Server Certificate**: `scripts/gen_cert.py server` issues server certificate
- **Client Certificate**: `scripts/gen_cert.py client` issues client certificate
- **Certificate Validation**: Both sides validate certificates
- **Invalid Certificate Rejection**: Self-signed/invalid certs are rejected with "BAD CERT" error

**Files:**
- `scripts/gen_ca.py` - Creates root CA
- `scripts/gen_cert.py` - Issues certificates
- `crypto_utils.py` - Validates certificates
- `test_invalid_cert.py` - Tests invalid cert rejection

---

### 2. Secure Registration & Login ✅
- **MySQL Database**: Schema in `database/schema.sql`
- **Encrypted Credentials**: Passwords sent encrypted (not plaintext)
- **Salted Hashing**: `SHA256(salt || password)` stored in database
- **Login Verification**: Certificate + salted hash verification

**Files:**
- `database/schema.sql` - MySQL schema
- `setup_database.py` - Database setup helper
- `server.py` - Registration/login logic
- `client.py` - Registration/login interface
- `test_db.py` - Database verification

---

### 3. Diffie-Hellman Key Exchange ✅
- **DH Exchange**: Client sends `p, g, A`, server sends `B`
- **Shared Secret**: Both compute `Ks`
- **Session Key**: `K = Trunc16(SHA256(Ks))` for AES-128
- **Unique Keys**: Each session has unique key

**Files:**
- `server.py` - Server-side DH implementation
- `client.py` - Client-side DH implementation
- `crypto_utils.py` - Key derivation function

---

### 4. Encrypted Chat Messages ✅
- **AES-128 Encryption**: PKCS#7 padding
- **Sequence Numbers**: Replay protection
- **Timestamps**: Message timing
- **SHA-256 Hashing**: Message integrity
- **RSA Signatures**: Digital signatures
- **Verification**: Server verifies all messages

**Files:**
- `crypto_utils.py` - AES encryption, RSA signatures
- `server.py` - Message verification
- `client.py` - Message encryption
- `test_tampering.py` - Tampering detection test
- `test_replay.py` - Replay attack test

---

### 5. Non-Repudiation ✅
- **Session Transcripts**: All messages stored
- **Transcript Hashing**: `SHA256(all transcript lines)`
- **RSA Signatures**: Hash signed with private key
- **Session Receipt**: JSON with hash + signature
- **Verification**: Transcript modification breaks signature

**Files:**
- `server.py` - Transcript and receipt generation
- `client.py` - Transcript and receipt generation
- `crypto_utils.py` - Transcript hashing
- `test_non_repudiation.py` - Receipt verification test

---

## 📁 File Structure

```
.
├── server.py                    # Main server implementation
├── client.py                    # Main client implementation
├── crypto_utils.py              # Cryptographic utilities
├── scripts/
│   ├── gen_ca.py               # CA generation
│   └── gen_cert.py             # Certificate generation
├── database/
│   └── schema.sql              # MySQL schema
├── certs/                      # Certificates (gitignored)
├── transcripts/               # Session transcripts (gitignored)
├── test_*.py                   # Test scripts
├── requirements.txt            # Dependencies
├── README.md                   # Main documentation
├── FILE_PURPOSE.md             # File purpose explanation
├── TESTING_GUIDE.md            # Testing instructions
└── ASSIGNMENT_SUMMARY.md       # This file
```

---

## 🚀 How to Run

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup database
python setup_database.py

# 3. Generate certificates
python scripts/gen_ca.py
python scripts/gen_cert.py server
python scripts/gen_cert.py client

# 4. Run system
python server.py    # Terminal 1
python client.py    # Terminal 2
```

### Run All Tests
```bash
python run_all_tests.py
```

---

## 📸 Testing Evidence Required

### 1. Wireshark Screenshot
- Capture traffic on port 9999
- Show encrypted payloads (no plaintext)
- Filter: `tcp.port == 9999`

### 2. Invalid Certificate Test
- Run: `python test_invalid_cert.py`
- Replace client cert with invalid cert
- Connect and show "BAD CERT" error

### 3. Tampering Test
- Send message from client
- Modify ciphertext in transit
- Show "SIG FAIL" error

### 4. Replay Test
- Send messages 1, 2, 3
- Resend message 2
- Show "REPLAY" error

### 5. Non-Repudiation Test
- Complete chat session
- View transcript and receipt
- Modify transcript
- Show hash mismatch

**See `TESTING_GUIDE.md` for detailed instructions.**

---

## 📝 Submission Checklist

- [x] **GitHub Repository** (private, ≥10 commits)
- [x] **MySQL Schema** (`database/schema.sql`)
- [x] **README.md** (how to run, setup, sample I/O)
- [ ] **Report** (`RollNumber-FullName-Report-A02.docx`)
- [ ] **Test Report** (`RollNumber-FullName-TestReport-A02.docx`)
- [ ] **Wireshark Screenshots**
- [ ] **Test Evidence** (invalid cert, tampering, replay, non-repudiation)

---

## 🔒 Security Features

- ✅ **Confidentiality**: AES-128 encryption
- ✅ **Integrity**: SHA-256 + RSA signatures
- ✅ **Authenticity**: X.509 certificate validation
- ✅ **Non-Repudiation**: Signed session receipts
- ✅ **Replay Protection**: Sequence number enforcement

---

## 📚 Documentation

- **README.md** - Main documentation with setup and usage
- **FILE_PURPOSE.md** - Explains each file's purpose and assignment goals
- **TESTING_GUIDE.md** - Detailed testing instructions for all required tests
- **ASSIGNMENT_SUMMARY.md** - This file (overview of completed work)

---

## ✅ All Tests Passing

```
[PASS] Certificate Validation: PASSED
[PASS] Database Setup: PASSED
[PASS] Invalid Certificate Test: PASSED
[PASS] Tampering Detection Test: PASSED
[PASS] Replay Attack Test: PASSED
[PASS] Non-Repudiation Test: PASSED
```

---

## 🎯 Assignment Goals Status

| Goal | Status | Implementation |
|------|--------|----------------|
| 1. CA and Certificates | ✅ | `scripts/gen_*.py`, `crypto_utils.py` |
| 2. Secure Registration & Login | ✅ | `database/schema.sql`, `server.py`, `client.py` |
| 3. Diffie-Hellman Key Exchange | ✅ | `server.py`, `client.py`, `crypto_utils.py` |
| 4. Encrypted Chat Messages | ✅ | `crypto_utils.py`, `server.py`, `client.py` |
| 5. Non-Repudiation | ✅ | `server.py`, `client.py`, `crypto_utils.py` |

**All assignment requirements are complete!** 🎉

---

## 📞 Support

For issues or questions:
1. Check `README.md` for setup instructions
2. Check `TESTING_GUIDE.md` for testing help
3. Check `FILE_PURPOSE.md` for file explanations
4. Run `python run_all_tests.py` to verify setup

---

**System is ready for submission!** ✅

