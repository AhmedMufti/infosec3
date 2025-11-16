# How to Run the Secure Chat System

## 🚀 Quick Start (3 Steps)

### Step 1: Install Packages
```bash
py -m pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
py setup_database.py
```

### Step 3: Run the System

**Open TWO terminal windows:**

**Terminal 1 - Server:**
```bash
py server.py
```

**Terminal 2 - Client:**
```bash
py client.py
```

---

## 📋 Detailed Instructions

### 1. Install Dependencies

**IMPORTANT:** Always use `py -m pip` (not just `pip`) to ensure packages install for the correct Python:

```bash
py -m pip install -r requirements.txt
```

This installs:
- `cryptography` - For encryption and certificates
- `pymysql` - For MySQL database
- `python-dotenv` - For environment variables  
- `python-docx` - For generating reports

### 2. Setup MySQL Database

**Option A: Automatic (Recommended)**
```bash
py setup_database.py
```

**Option B: Manual**
```bash
mysql -u root -p < database/schema.sql
```

### 3. Generate Certificates

**Option A: Use setup script**
```bash
py setup.py
```

**Option B: Manual**
```bash
py scripts/gen_ca.py
py scripts/gen_cert.py server
py scripts/gen_cert.py client
```

### 4. Create .env File

Create a file named `.env` in the project folder:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=securechat
SERVER_HOST=localhost
SERVER_PORT=9999
```

**Replace `your_password_here` with your MySQL password!**

### 5. Run the System

You need **TWO terminal windows** open:

**Terminal 1 - Start Server:**
```bash
cd D:\downloads\infosec3
py server.py
```

Wait for: `Server listening on localhost:9999`

**Terminal 2 - Start Client:**
```bash
cd D:\downloads\infosec3
py client.py
```

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pymysql'"

**Fix:**
```bash
py -m pip install pymysql
```

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Fix:**
```bash
py -m pip install python-dotenv
```

**Note:** The package is `python-dotenv` but you import it as `dotenv`:
```python
from dotenv import load_dotenv  # This is correct!
```

### Error: Packages installed but still not found

**Problem:** You used `pip` instead of `py -m pip`

**Solution:** Always use `py -m pip`:
```bash
# Wrong:
pip install pymysql

# Correct:
py -m pip install pymysql
```

### Error: Database connection failed

**Check:**
1. MySQL is running
2. `.env` file exists with correct password
3. Database `securechat` exists

**Test database:**
```bash
py test_db.py
```

### Error: Certificates not found

**Fix:**
```bash
py setup.py
```

---

## ✅ Verify Installation

Test if everything is installed correctly:

```bash
py -c "import pymysql; print('pymysql: OK')"
py -c "from dotenv import load_dotenv; print('dotenv: OK')"
py -c "import cryptography; print('cryptography: OK')"
```

All should print "OK".

---

## 📝 Complete Example Session

```bash
# 1. Install packages
py -m pip install -r requirements.txt

# 2. Setup database
py setup_database.py

# 3. Generate certificates (if not done)
py setup.py

# 4. Start server (Terminal 1)
py server.py

# 5. Start client (Terminal 2 - NEW TERMINAL)
py client.py

# 6. In client, register a new user:
#    - Choose option 1 (Register)
#    - Enter email, username, password
#    - Send messages
#    - Type 'quit' to end
```

---

## 🎯 Key Points

1. **Always use `py -m pip`** instead of just `pip`
2. **Use `py` command** to run Python scripts (or `python` if `py` doesn't work)
3. **Two terminals needed** - one for server, one for client
4. **Create `.env` file** with your MySQL password
5. **MySQL must be running** before starting the server

---

## 🆘 Still Having Issues?

1. Check Python version: `py --version` (should be 3.8+)
2. Check packages: `py -m pip list`
3. Check database: `py test_db.py`
4. Check certificates: `dir certs\`

---

**You're all set!** 🎉

