# Test 5: Non-Repudiation Test - Simple Guide

## What You're Testing
Verify that session receipts prove the conversation happened and detect if transcripts are modified.

## Method: Complete Session and Verify Receipt

### Step 1: Complete a Chat Session
```bash
# Terminal 1
py server.py

# Terminal 2  
py client.py
```

1. Register and login
2. Send 3-4 messages
3. Type `quit` to end session
4. Both server and client will generate transcripts

### Step 2: Find Transcript Files

Transcripts are saved in `transcripts/` folder:
- `client_username_timestamp.txt`
- `server_username_timestamp.txt`

### Step 3: View a Transcript

Open one of the transcript files. It should look like:
```
1|1234567890|base64ciphertext...|base64signature...|fingerprint
2|1234567891|base64ciphertext...|base64signature...|fingerprint
--- RECEIPT ---
{"type":"receipt","transcript_sha256":"abc123...","signature":"xyz789..."}
```

### Step 4: Verify Receipt (Automatic Test)

Run the test script:
```bash
py test_non_repudiation.py
```

This will:
- Load the transcript
- Compute the hash
- Compare with receipt hash
- Show if they match

**Expected output:**
```
[OK] Hash matches - Transcript is intact
```

### Step 5: Test Tampering Detection

**Modify the transcript file:**
1. Open the transcript file in a text editor
2. Add something to any line, for example:
   ```
   1|1234567890|base64ciphertext...|base64signature...|fingerprint TAMPERED
   ```
3. Save the file

**Run verification again:**
```bash
py test_non_repudiation.py
```

**Expected output:**
```
[FAIL] Hash mismatch - Transcript has been modified!
[FAIL] Hash changed - Tampering detected!
```

### Step 6: Manual Verification

You can also verify manually:

1. **Original transcript:**
   - Hash in receipt: `abc123...`
   - Computed hash: `abc123...`
   - ✅ Match = Transcript is intact

2. **Modified transcript:**
   - Hash in receipt: `abc123...`
   - Computed hash: `xyz789...` (different!)
   - ❌ Mismatch = Transcript was tampered with

---

## What's Happening?

1. **During session:** All messages are logged to transcript
2. **At end:** System computes `SHA256(all transcript lines)` = hash
3. **Receipt created:** Hash is signed with RSA private key → Receipt contains hash + signature
4. **Verification:** Anyone can recompute hash and compare with receipt
5. **Tampering detection:** If transcript is modified, hash changes → mismatch detected

This proves:
- ✅ The conversation happened (receipt exists)
- ✅ No one can deny it (signed with private key)
- ✅ Any modification is detected (hash changes)

---

## Screenshot for Report

Take screenshots of:
1. Original transcript file (showing messages and receipt)
2. Verification showing "Hash matches"
3. Modified transcript (with your change)
4. Verification showing "Hash mismatch - Tampering detected!"

---

## Quick Test Commands

```bash
# 1. Complete a chat session (register, login, send messages, quit)

# 2. List transcripts
dir transcripts

# 3. View a transcript
type transcripts\client_*.txt

# 4. Run verification
py test_non_repudiation.py

# 5. Modify transcript (add "TAMPERED" to any line)

# 6. Run verification again
py test_non_repudiation.py
```

---

**That's it!** This proves your system provides non-repudiation. ✅

