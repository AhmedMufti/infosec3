# Expected System Output Demonstration

This document shows what the output looks like when running the secure chat system.

## Step 1: Generate Certificates

### CA Generation
```bash
$ python scripts/gen_ca.py
Generating CA private key...
CA private key saved to certs/ca_key.pem
Generating CA certificate...
CA certificate saved to certs/ca_cert.pem

CA Certificate Information:
  Subject: <Name(C=PK,ST=State,L=City,O=FAST-NUCES,OU=CS,CN=SecureChat-CA,emailAddress=ca@securechat.local)>
  Serial Number: 12345678901234567890
  Valid From: 2025-01-01 00:00:00
  Valid To: 2035-01-01 00:00:00
  Key Size: 2048 bits

CA created successfully!
```

### Server Certificate Generation
```bash
$ python scripts/gen_cert.py server
Generating server private key...
server private key saved to certs/server_key.pem
Generating server certificate...
server certificate saved to certs/server_cert.pem

SERVER Certificate Information:
  Subject: <Name(C=PK,ST=State,L=City,O=FAST-NUCES,OU=CS,CN=server,emailAddress=server@securechat.local)>
  Issuer: <Name(C=PK,ST=State,L=City,O=FAST-NUCES,OU=CS,CN=SecureChat-CA,emailAddress=ca@securechat.local)>
  Serial Number: 98765432109876543210
  Valid From: 2025-01-01 00:00:00
  Valid To: 2026-01-01 00:00:00
  Key Size: 2048 bits

SERVER certificate created successfully!
```

### Client Certificate Generation
```bash
$ python scripts/gen_cert.py client
Generating client private key...
client private key saved to certs/client_key.pem
Generating client certificate...
client certificate saved to certs/client_cert.pem

CLIENT Certificate Information:
  Subject: <Name(C=PK,ST=State,L=City,O=FAST-NUCES,OU=CS,CN=client,emailAddress=client@securechat.local)>
  Issuer: <Name(C=PK,ST=State,L=City,O=FAST-NUCES,OU=CS,CN=SecureChat-CA,emailAddress=ca@securechat.local)>
  Serial Number: 11223344556677889900
  Valid From: 2025-01-01 00:00:00
  Valid To: 2026-01-01 00:00:00
  Key Size: 2048 bits

CLIENT certificate created successfully!
```

## Step 2: Start Server

```bash
$ python server.py
Connected to database: securechat
Server listening on localhost:9999
```

## Step 3: Start Client and Connect

```bash
$ python client.py
Connected to server localhost:9999
Control plane: Certificates exchanged and validated

1. Register
2. Login
Enter choice (1/2): 1
```

## Step 4: User Registration

```
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
How are you?
[Server]: Message 2 received
quit
Session receipt generated: transcripts/client_alice_20250101_120000.txt
```

## Step 5: Server Output During Chat

```
New connection from ('127.0.0.1', 54321)
Control plane: Certificates exchanged and validated
User registered: alice (alice@example.com)
Key agreement: Session key established
Data plane: Starting encrypted chat
Waiting for messages from client...
[alice]: Hello, this is a test message
[alice]: How are you?
Client ('127.0.0.1', 54321) disconnected
Session receipt generated: transcripts/server_alice_20250101_120000.txt
```

## Step 6: User Login

```bash
$ python client.py
Connected to server localhost:9999
Control plane: Certificates exchanged and validated

1. Register
2. Login
Enter choice (1/2): 2
Email: alice@example.com
Password: ********
Login successful!
Key agreement: Session key established

Data plane: Starting encrypted chat
Type messages and press Enter to send
Type 'quit' to end the session

This is an encrypted message
[Server]: Message 1 received
Another message
[Server]: Message 2 received
quit

Session receipt generated: transcripts/client_alice_20250101_120100.txt
```

## Step 7: Error Scenarios

### Invalid Certificate
```
Connected to server localhost:9999
Error: BAD CERT: Self-signed certificate rejected
```

### Replay Attack Detection
```
[alice]: Hello
[alice]: World
REPLAY: Invalid sequence number
```

### Signature Failure
```
[alice]: Test message
SIG FAIL: Invalid signature
```

### Invalid Login
```
Email: wrong@example.com
Password: wrongpass
Login failed: Invalid credentials
```

## Step 8: Session Transcript Example

File: `transcripts/client_alice_20250101_120000.txt`
```
1|1704110400000|aGVsbG8gd29ybGQ=|signature1|abc123...
2|1704110401000|dGVzdCBtZXNzYWdl|signature2|abc123...
--- RECEIPT ---
{
  "type": "receipt",
  "peer": "client",
  "first_seq": 1,
  "last_seq": 2,
  "transcript_sha256": "a1b2c3d4e5f6...",
  "sig": "signature_base64..."
}
```

## Step 9: Certificate Validation Test

```bash
$ openssl x509 -in certs/server_cert.pem -text -noout
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            12:34:56:78:90:ab:cd:ef
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=PK, ST=State, L=City, O=FAST-NUCES, OU=CS, CN=SecureChat-CA
        Validity
            Not Before: Jan  1 00:00:00 2025 GMT
            Not After : Jan  1 00:00:00 2026 GMT
        Subject: C=PK, ST=State, L=City, O=FAST-NUCES, OU=CS, CN=server
        ...
```

## Summary

The system demonstrates:
- ✅ Certificate generation and validation
- ✅ Secure user registration and login
- ✅ Diffie-Hellman key exchange
- ✅ Encrypted message transmission
- ✅ Message integrity verification
- ✅ Replay attack prevention
- ✅ Session transcript generation
- ✅ Non-repudiation receipts

All communication is encrypted and authenticated, meeting all CIANR requirements.

