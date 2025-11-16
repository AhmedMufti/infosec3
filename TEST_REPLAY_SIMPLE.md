# Test 4: Replay Attack Test - Simple Guide

## What You're Testing
Verify that if someone tries to resend an old message, the server detects it and rejects it with "REPLAY: Invalid sequence number".

## Easiest Method: Modify Client Code Temporarily

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

### Step 3: Send Some Messages
- Send message 1: "Hello"
- Send message 2: "How are you?"
- Send message 3: "Test message"

### Step 4: Modify client.py to Simulate Replay

Open `client.py` and find the `send_message` method (around line 380-410).

Find this code:
```python
message = {
    'type': 'msg',
    'seqno': self.seqno,
    'ts': timestamp,
    'ct': ciphertext_b64,
    'sig': signature_b64
}

# Send message
self.send_message(message)
```

**Right after sending, add this code to resend with old seqno:**
```python
# Send message
self.send_message(message)

# REPLAY TEST: Try to resend with old sequence number
print("Attempting replay attack...")
old_seqno = self.seqno - 1  # Use previous sequence number
replay_message = {
    'type': 'msg',
    'seqno': old_seqno,  # Replay with old seqno
    'ts': timestamp,
    'ct': ciphertext_b64,
    'sig': signature_b64
}
self.send_message(replay_message)
```

### Step 5: Restart Client
- Stop the client (Ctrl+C)
- Start it again: `py client.py`
- Login and send a message

### Step 6: Expected Result
**Server should show:**
```
REPLAY: Invalid sequence number
```

**Client should show:**
```
Error: REPLAY: Invalid sequence number
```

### Step 7: Remove Replay Code
- Remove the replay test code you added
- Restart client
- System works normally again

---

## Alternative: Manual Sequence Number Test

If you don't want to modify code:

1. Send messages 1, 2, 3 normally
2. Note the sequence numbers in server logs
3. The server tracks `seqno` - it expects each new message to have `seqno > last_seqno`
4. If you could somehow send message with seqno=2 again, it would be rejected

---

## What's Happening?

1. **Normal flow:** Message 1 (seqno=1) → Message 2 (seqno=2) → Message 3 (seqno=3) → All accepted
2. **Replay flow:** Message 1 (seqno=1) → Message 2 (seqno=2) → **Message 2 again (seqno=2)** → Server checks: `2 <= 2` → **REJECTED with "REPLAY"**

The server tracks the last sequence number received. Any message with `seqno <= last_seqno` is considered a replay and rejected.

---

## Screenshot for Report

Take screenshots of:
1. The modified code (showing replay attempt)
2. Server output showing "REPLAY: Invalid sequence number"
3. Client output showing the error

---

**That's it!** This proves your system prevents replay attacks. ✅

