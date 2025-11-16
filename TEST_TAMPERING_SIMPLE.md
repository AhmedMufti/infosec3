# Test 3: Tampering Test - Simple Guide

## What You're Testing
Verify that if someone modifies a message in transit, the server detects it and rejects it with "SIG FAIL: Invalid signature".

## Easiest Method: Modify Server Code Temporarily

### Step 1: Start Server and Client
```bash
# Terminal 1
py server.py

# Terminal 2  
py client.py
```

### Step 2: Register and Login
- Register a new user
- Login
- Wait for "Key agreement: Session key established"

### Step 3: Modify server.py to Simulate Tampering

Open `server.py` and find the `data_plane` method (around line 430-500).

Find this code (where it receives the message):
```python
ciphertext = base64.b64decode(ciphertext_b64)
```

**Add these lines RIGHT AFTER it:**
```python
ciphertext = base64.b64decode(ciphertext_b64)

# TAMPERING TEST: Modify ciphertext
ciphertext = bytearray(ciphertext)
ciphertext[20] ^= 0xFF  # Flip a bit at position 20
ciphertext = bytes(ciphertext)
```

### Step 4: Restart Server
- Stop the server (Ctrl+C)
- Start it again: `py server.py`

### Step 5: Send a Message from Client
- In the client, type a message and press Enter

### Step 6: Expected Result
**Server should show:**
```
SIG FAIL: Invalid signature
```

**Client should show:**
```
Error: SIG FAIL: Invalid signature
```

### Step 7: Remove Tampering Code
- Remove the tampering lines you added
- Restart server
- System works normally again

---

## Alternative: Use a Proxy Tool

If you have Burp Suite or similar:
1. Configure client to use proxy
2. Intercept message
3. Modify ciphertext in proxy
4. Forward to server
5. Server should reject with "SIG FAIL"

---

## What's Happening?

1. **Normal flow:** Client encrypts message → signs it → sends to server → server verifies signature → accepts
2. **Tampered flow:** Client encrypts message → signs it → **attacker modifies ciphertext** → server verifies signature → **signature doesn't match** → rejects with "SIG FAIL"

The signature is computed from the original ciphertext, so any modification breaks the signature verification.

---

## Screenshot for Report

Take screenshots of:
1. The modified code (showing tampering lines)
2. Server output showing "SIG FAIL: Invalid signature"
3. Client output showing the error

---

**That's it!** This proves your system detects message tampering. ✅

