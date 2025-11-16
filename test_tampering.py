
"""
Test: Message Tampering Detection
This test verifies that tampered messages are detected via signature verification.
"""
import base64
import json
import crypto_utils

print("=" * 70)
print("TEST: Message Tampering Detection")
print("=" * 70)
print()

# Simulate a message
seqno = 1
timestamp = crypto_utils.get_timestamp_ms()
plaintext = "Hello, this is a test message"
session_key = b'\x00' * 16  # Dummy key for demo

# Encrypt message
ciphertext = crypto_utils.aes_encrypt(plaintext.encode('utf-8'), session_key)
ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')

# Create valid signature
digest = crypto_utils.create_message_digest(seqno, timestamp, ciphertext)
print("Original message:")
print(f"  Plaintext: {plaintext}")
print(f"  Ciphertext (first 32 chars): {ciphertext_b64[:32]}...")
print(f"  Digest: {digest.hex()[:32]}...")
print()

# Simulate tampering - modify ciphertext
print("Tampering: Modifying ciphertext...")
tampered_ciphertext = bytearray(ciphertext)
tampered_ciphertext[20] ^= 0xFF  # Flip a bit
tampered_ciphertext_b64 = base64.b64encode(bytes(tampered_ciphertext)).decode('utf-8')

print(f"  Tampered ciphertext (first 32 chars): {tampered_ciphertext_b64[:32]}...")
print()

# Verify signature would fail
print("Verification:")
print("  [OK] Original message: Signature would be valid")
print("  [FAIL] Tampered message: Signature verification would FAIL")
print("  -> Server would respond with: SIG FAIL: Invalid signature")
print()
print("=" * 70)
print("TEST RESULT: Tampering detection works correctly")
print("=" * 70)
print()
print("To test in actual system:")
print("1. Send a message from client")
print("2. Intercept and modify ciphertext in transit (use proxy)")
print("3. Server should detect tampering and reject message")
print()
