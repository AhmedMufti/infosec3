# Quick Start Guide - How to Run the System

## ⚠️ Important: Python Interpreter Issue

On Windows, you might have multiple Python installations. Make sure you use the **same Python** for installing packages and running scripts.

## ✅ Solution: Use `py -m pip` for Installation

Always use `py -m pip` instead of just `pip` to ensure packages are installed for the correct Python interpreter.

---

## Step-by-Step Instructions

### Step 1: Install Dependencies

```bash
py -m pip install -r requirements.txt
```

This installs:
- `cryptography` - For certificates and encryption
- `pymysql` - For MySQL database
- `python-dotenv` - For environment variables
- `python-docx` - For report generation

### Step 2: Set Up Database

**Option A: Using Python script (Recommended)**
```bash
py setup_database.py
```

**Option B: Using MySQL command**
```bash
mysql -u root -p < database/schema.sql
```

### Step 3: Generate Certificates

```bash
py scripts/gen_ca.py
py scripts/gen_cert.py server
py scripts/gen_cert.py client
```

**OR use the setup script:**
```bash
py setup.py
```

### Step 4: Create .env File

Create a file named `.env` in the project root with:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=securechat
SERVER_HOST=localhost
SERVER_PORT=9999
```

Replace `your_mysql_password` with your actual MySQL password.

### Step 5: Run the System

**Terminal 1 - Start Server:**
```bash
py server.py
```

**Terminal 2 - Start Client:**
```bash
py client.py
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pymysql'"

**Solution:**
```bash
py -m pip install pymysql
```

### Problem: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```bash
py -m pip install python-dotenv
```

### Problem: Packages installed but still not found

**Solution:** Use `py -m pip` instead of `pip`:
```bash
# Wrong:
pip install pymysql

# Correct:
py -m pip install pymysql
```

### Problem: Database connection error

**Solution:**
1. Make sure MySQL is running
2. Check your `.env` file has correct credentials
3. Verify database exists: `mysql -u root -p -e "SHOW DATABASES;"`

---

## Quick Commands Reference

```bash
# Install all dependencies
py -m pip install -r requirements.txt

# Setup database
py setup_database.py

# Generate certificates
py setup.py

# Run server
py server.py

# Run client (in another terminal)
py client.py

# Run all tests
py run_all_tests.py

# Generate reports
py generate_reports.py
```

---

## Alternative: Use `python` instead of `py`

If `py` doesn't work, try using `python`:

```bash
python -m pip install -r requirements.txt
python server.py
python client.py
```

---

## Complete Setup in One Go

```bash
# 1. Install dependencies
py -m pip install -r requirements.txt

# 2. Setup database (make sure MySQL is running)
py setup_database.py

# 3. Generate certificates
py setup.py

# 4. Create .env file (edit with your MySQL password)
# Then run:
py server.py    # Terminal 1
py client.py    # Terminal 2
```

---

**That's it! The system should now work correctly.** 🎉

