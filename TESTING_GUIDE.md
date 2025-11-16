# Testing Guide - Assignment Requirements
#updated

This guide shows how to perform all required tests for the assignment.

## Required Tests

1. ✅ Wireshark screenshot (encrypted traffic)
2. ✅ Invalid certificate test → BAD CERT
3. ✅ Tampering test → SIG FAIL
4. ✅ Replay test → REPLAY
5. ✅ Non-repudiation test → signature breaks on modification

---

## Test 1: Wireshark - Encrypted Traffic

### Setup
1. Install Wireshark
2. Start capturing on `localhost` or `127.0.0.1`
3. Filter: `tcp.port == 9999`

### Steps
1. Start server: `python server.py`
2. Start client: `python client.py`
3. Register and send messages
4. Capture traffic in Wireshark

### What to Look For
- ✅ All payloads are encrypted (no plaintext)
- ✅ No passwords visible
- ✅ No message content visible
- ✅ Only encrypted ciphertext visible

### Screenshot Requirements
- Show Wireshark capture window
- Highlight encrypted payloads
- Show filter used: `tcp.port == 9999`
- Annotate: "All traffic encrypted - no plaintext visible"

---

## Test 2: Invalid Certificate Test

### Method 1: Using Test Script
```bash
python test_invalid_cert.py
```

### Method 2: Manual Test

1. **Create invalid certificate:**
   ```bash
   python test_invalid_cert.py
   ```

2. **Replace client certificate temporarily:**
   ```bash
   # Backup original
   copy certs\client_cert.pem certs\client_cert.pem.backup
   
   # Use invalid cert
   copy certs\invalid_cert.pem certs\client_cert.pem
   ```

3. **Try to connect:**
   ```bash
   python client.py
   ```

4. **Expected Result:**
   ```
   Error from server: BAD CERT: Self-signed certificate rejected
   ```

5. **Restore original:**
   ```bash
   copy certs\client_cert.pem.backup certs\client_cert.pem
   ```

### Screenshot Requirements
- Show client error message: "BAD CERT: Self-signed certificate rejected"
- Show server log: "Control plane: Client certificate validation failed"

---

## Test 3: Tampering Test

### Setup
1. Start server: `python server.py`
2. Start client: `python client.py`
3. Register and establish session

### Method 1: Using Proxy/Interceptor

1. **Use a proxy tool** (e.g., Burp Suite, mitmproxy)
2. **Intercept a message**
3. **Modify ciphertext** (flip a bit)
4. **Forward modified message**

### Method 2: Manual Code Modification

1. **Modify `server.py` temporarily:**
   ```python
   # In data_plane method, after receiving ciphertext:
   ciphertext = base64.b64decode(ciphertext_b64)
   # Tamper with it
   ciphertext = bytearray(ciphertext)
   ciphertext[10] ^= 0xFF  # Flip a bit
   ciphertext = bytes(ciphertext)
   ```

2. **Send message from client**
3. **Expected Result:**
   ```
   [Server]: SIG FAIL: Invalid signature
   ```

### Method 3: Using Test Script
```bash
python test_tampering.py
```

### Screenshot Requirements
- Show tampered message
- Show server error: "SIG FAIL: Invalid signature"
- Explain: "Message tampering detected via signature verification"

---

## Test 4: Replay Attack Test

### Setup
1. Start server: `python server.py`
2. Start client: `python client.py`
3. Register and send messages 1, 2, 3

### Method 1: Manual Replay

1. **Capture a message** (use Wireshark or logging)
2. **Send message 2 again** (same seqno)
3. **Expected Result:**
   ```
   [Server]: REPLAY: Invalid sequence number
   ```

### Method 2: Code Modification

1. **Modify client to resend message:**
   ```python
   # After sending message 2, resend it
   self.send_message(message)  # Send again
   ```

2. **Expected Result:**
   ```
   Error: REPLAY: Invalid sequence number
   ```

### Method 3: Using Test Script
```bash
python test_replay.py
```

### Screenshot Requirements
- Show replayed message (same seqno)
- Show server error: "REPLAY: Invalid sequence number"
- Explain: "Replay attack prevented via sequence number checking"

---

## Test 5: Non-Repudiation Test

### Setup
1. Complete a chat session
2. Generate transcript and receipt

### Steps

1. **View transcript:**
   ```bash
   # Check transcripts directory
   dir transcripts
   
   # View a transcript
   type transcripts\client_ahmed_*.txt
   ```

2. **Verify receipt:**
   ```bash
   python test_non_repudiation.py
   ```

3. **Modify transcript:**
   - Open transcript file
   - Change a message or add a line
   - Save file

4. **Verify signature breaks:**
   ```python
   # The hash will change
   # Signature verification will fail
   ```

### Manual Verification Script

Create `verify_receipt.py`:
```python
import json
import crypto_utils
from crypto_utils import load_certificate

# Load transcript
with open('transcripts/client_ahmed_*.txt', 'r') as f:
    content = f.read()

parts = content.split('--- RECEIPT ---')
transcript_lines = [l for l in parts[0].strip().split('\n') if l]
receipt = json.loads(parts[1].strip())

# Compute hash
computed_hash = crypto_utils.compute_transcript_hash(transcript_lines)
receipt_hash = receipt['transcript_sha256']

print(f"Computed: {computed_hash}")
print(f"Receipt:  {receipt_hash}")
print(f"Match: {computed_hash == receipt_hash}")
```

### Screenshot Requirements
- Show original transcript
- Show receipt with hash and signature
- Show modified transcript
- Show hash mismatch
- Explain: "Transcript modification invalidates receipt signature"

---

## Running All Tests

### Automated Test Suite
```bash
python run_all_tests.py
```

This runs:
- Certificate validation test
- Database setup test
- Invalid certificate test
- Tampering test
- Replay test
- Non-repudiation test

### Manual Test Sequence

1. **Start server:**
   ```bash
   python server.py
   ```

2. **Test invalid cert:**
   ```bash
   # In another terminal
   python test_invalid_cert.py
   # Follow instructions to test
   ```

3. **Test normal flow:**
   ```bash
   python client.py
   # Register, login, send messages
   ```

4. **Test tampering:**
   - Use proxy or modify code
   - Verify SIG FAIL

5. **Test replay:**
   - Resend a message
   - Verify REPLAY error

6. **Test non-repudiation:**
   ```bash
   python test_non_repudiation.py
   # Modify transcript and verify signature breaks
   ```

---

## Test Evidence Checklist

For your Test Report, include screenshots of:

- [ ] **Wireshark Capture**
  - Encrypted payloads visible
  - Filter shown: `tcp.port == 9999`
  - No plaintext visible

- [ ] **Invalid Certificate Test**
  - Server log showing "BAD CERT"
  - Client error message
  - Explanation of why cert was rejected

- [ ] **Tampering Test**
  - Original message
  - Tampered message
  - Server error: "SIG FAIL"
  - Explanation of detection

- [ ] **Replay Test**
  - Original message sequence
  - Replayed message
  - Server error: "REPLAY"
  - Explanation of prevention

- [ ] **Non-Repudiation Test**
  - Original transcript
  - Receipt with hash and signature
  - Modified transcript
  - Hash mismatch
  - Signature verification failure
  - Explanation of non-repudiation

---

## Quick Test Commands

```bash
# Setup
python setup_database.py
python scripts/gen_ca.py
python scripts/gen_cert.py server
python scripts/gen_cert.py client

# Run all tests
python run_all_tests.py

# Individual tests
python test_cert_validation.py
python test_db.py
python test_invalid_cert.py
python test_tampering.py
python test_replay.py
python test_non_repudiation.py

# Run system
python server.py  # Terminal 1
python client.py  # Terminal 2
```

---

## Troubleshooting Tests

### Certificate Tests Fail
- Ensure certificates are generated
- Check certificate expiry dates
- Verify CA certificate exists

### Database Tests Fail
- Check MySQL is running
- Verify database exists
- Check .env file credentials

### Message Tests Fail
- Ensure session is established
- Check sequence numbers
- Verify signatures are working

---

## Test Report Template

For your `TestReport-A02.docx`, structure it as:

1. **Introduction**
   - Testing methodology
   - Tools used (Wireshark, etc.)

2. **Test 1: Wireshark Evidence**
   - Screenshot
   - Explanation
   - Filter used

3. **Test 2: Invalid Certificate**
   - Screenshot
   - Error message
   - Explanation

4. **Test 3: Tampering Detection**
   - Screenshot
   - Error message
   - Explanation

5. **Test 4: Replay Prevention**
   - Screenshot
   - Error message
   - Explanation

6. **Test 5: Non-Repudiation**
   - Screenshot
   - Verification steps
   - Explanation

7. **Conclusion**
   - All tests passed
   - System security verified

---

This completes all required testing for the assignment! ✅

