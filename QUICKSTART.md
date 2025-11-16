# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **MySQL Server** installed and running
3. **Git** (for version control)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up MySQL Database

```bash
mysql -u root -p < database/schema.sql
```

Or manually:
```sql
CREATE DATABASE securechat;
USE securechat;
-- Run the SQL from database/schema.sql
```

## Step 3: Configure Environment

Create a `.env` file in the project root:

```env
# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=securechat

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=9999
```

## Step 4: Generate Certificates

```bash
# Generate CA
python scripts/gen_ca.py

# Generate server certificate
python scripts/gen_cert.py server

# Generate client certificate
python scripts/gen_cert.py client
```

## Step 5: Run the System

### Terminal 1: Start Server
```bash
python server.py
```

You should see:
```
Connected to database: securechat
Server listening on localhost:9999
```

### Terminal 2: Start Client
```bash
python client.py
```

You should see:
```
Connected to server localhost:9999
Control plane: Certificates exchanged and validated

1. Register
2. Login
Enter choice (1/2):
```

## Step 6: Test the System

### Register a New User
1. Choose option `1` (Register)
2. Enter email: `test@example.com`
3. Enter username: `testuser`
4. Enter password: `testpass123`
5. You should see: "Registration successful!"

### Login
1. Choose option `2` (Login)
2. Enter email: `test@example.com`
3. Enter password: `testpass123`
4. You should see: "Login successful!"
5. You should see: "Key agreement: Session key established"

### Send Messages
1. Type a message and press Enter
2. Server should receive and display the message
3. Type `quit` to end the session

### Verify Session Transcript
1. Check the `transcripts/` directory
2. You should see transcript files with session data
3. Each transcript includes a signed receipt

## Troubleshooting

### Certificate Errors
- Make sure you've generated all certificates
- Check that certificate files exist in `certs/` directory
- Verify certificate validity: `openssl x509 -in certs/server_cert.pem -text -noout`

### Database Connection Errors
- Verify MySQL is running: `mysql -u root -p`
- Check database exists: `SHOW DATABASES;`
- Verify `.env` file has correct credentials

### Port Already in Use
- Change `SERVER_PORT` in `.env` file
- Or kill the process using port 9999: `netstat -ano | findstr :9999` (Windows) or `lsof -i :9999` (Linux/Mac)

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

## Next Steps

1. Read `README.md` for detailed documentation
2. Read `VERIFICATION.md` for testing procedures
3. Read `IMPLEMENTATION_SUMMARY.md` for implementation details
4. Test with Wireshark to verify encryption
5. Test certificate validation with invalid certificates
6. Test replay and tampering detection

## Security Notes

- **Never commit** certificate files or private keys to Git
- **Never commit** `.env` file with real credentials
- Use strong passwords for database
- Keep certificates secure and don't share private keys
- Regularly rotate certificates in production

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the documentation files
3. Check GitHub issues (if using GitHub)
4. Review the assignment requirements



