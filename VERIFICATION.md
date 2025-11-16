# Verification and Testing Guide

## Pre-requisites Check

1. **Python Environment**
   ```bash
   python --version  # Should be 3.8+
   pip list | grep -E "cryptography|pymysql|python-dotenv"
   ```

2. **MySQL Database**
   ```bash
   mysql --version
   mysql -u root -p -e "SHOW DATABASES;" | grep securechat
   ```

3. **Certificates**
   ```bash
   ls -la certs/
   # Should have: ca_cert.pem, ca_key.pem, server_cert.pem, server_key.pem, client_cert.pem, client_key.pem
   ```

## Setup Verification

1. **Generate CA and Certificates**
   ```bash
   python scripts/gen_ca.py
   python scripts/gen_cert.py server
   python scripts/gen_cert.py client
   ```

2. **Verify Certificates**
   ```bash
   openssl x509 -in certs/ca_cert.pem -text -noout
   openssl x509 -in certs/server_cert.pem -text -noout
   openssl x509 -in certs/client_cert.pem -text -noout
   ```

3. **Database Setup**
   ```bash
   mysql -u root -p < database/schema.sql
   mysql -u root -p -e "USE securechat; SHOW TABLES;"
   ```

## Functional Testing

### Test 1: Certificate Validation
1. Start server: `python server.py`
2. Start client: `python client.py`
3. Verify mutual certificate exchange
4. Expected: "Control plane: Certificates exchanged and validated"

### Test 2: User Registration
1. Connect client to server
2. Choose option 1 (Register)
3. Enter email, username, password
4. Expected: "Registration successful!"
5. Verify in database: `mysql -u root -p -e "USE securechat; SELECT * FROM users;"`

### Test 3: User Login
1. Connect client to server
2. Choose option 2 (Login)
3. Enter registered email and password
4. Expected: "Login successful!"

### Test 4: Key Exchange
1. After successful login
2. Verify DH key exchange
3. Expected: "Key agreement: Session key established"

### Test 5: Encrypted Messaging
1. Send messages from client
2. Verify server receives and decrypts messages
3. Check Wireshark for encrypted payloads
4. Expected: No plaintext in network traffic

### Test 6: Message Integrity
1. Send a message from client
2. Verify signature validation on server
3. Expected: Messages are verified and accepted

### Test 7: Replay Protection
1. Capture a message
2. Try to resend it
3. Expected: "REPLAY: Invalid sequence number"

### Test 8: Tampering Detection
1. Modify ciphertext in transit (use proxy)
2. Expected: "SIG FAIL: Invalid signature"

### Test 9: Session Transcript
1. Complete a chat session
2. Check transcripts directory
3. Verify transcript file is created
4. Expected: `transcripts/client_<username>_<timestamp>.txt`

### Test 10: Non-Repudiation Receipt
1. End chat session
2. Verify receipt is generated
3. Check receipt signature
4. Expected: Valid receipt with signed transcript hash

## Security Testing

### Invalid Certificate Test
1. Create a self-signed certificate
2. Try to connect with it
3. Expected: "BAD CERT: Self-signed certificate rejected"

### Expired Certificate Test
1. Create an expired certificate
2. Try to connect with it
3. Expected: "BAD CERT: Certificate expired"

### Invalid Signature Test
1. Modify message signature
2. Send message
3. Expected: "SIG FAIL: Invalid signature"

## Wireshark Testing

1. Start Wireshark capture on localhost
2. Filter: `tcp.port == 9999`
3. Start server and client
4. Send messages
5. Verify:
   - All payloads are encrypted
   - No plaintext passwords
   - No plaintext messages
   - Certificate exchange is visible but certificates are valid

## Performance Testing

1. Measure connection time
2. Measure message encryption/decryption time
3. Measure signature verification time
4. Test with multiple concurrent clients

## Known Issues and Limitations

1. **Temporary DH Key**: The assignment requires encryption of registration/login with a temporary DH key, but the current implementation sends them without encryption for simplicity. This should be enhanced.

2. **Server Messages**: The server currently only receives messages. Bidirectional chat can be added.

3. **Concurrent Clients**: The server handles one client at a time. Threading is implemented but needs testing.

4. **Error Handling**: Some error cases may need more robust handling.

## Next Steps

1. Add temporary DH key exchange for registration/login encryption
2. Implement bidirectional chat (server can send messages)
3. Add more comprehensive error handling
4. Add logging for audit trail
5. Add configuration validation
6. Add unit tests



