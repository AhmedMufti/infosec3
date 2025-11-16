# Database Schema and Sample Records - Submission Guide

## What to Submit

The assignment requires:
1. **MySQL Schema** - The database structure (tables, columns, etc.)
2. **Sample Records** - Example data showing what actual records look like

---

## Files to Submit

### 1. Schema File (Required)
**File:** `database/schema.sql`

This file contains:
- Database creation statement
- Table creation with all columns
- Indexes and constraints
- Data types and sizes

**What it shows:**
- Database structure
- Table schema (users table)
- Column definitions (email, username, salt, pwd_hash, etc.)

### 2. Sample Records File (Required)
**File:** `database/sample_records.sql`

This file contains:
- Example INSERT statements
- Sample user records with:
  - Email addresses
  - Usernames
  - Salt values (16 bytes, shown as hex)
  - Password hashes (SHA256, 64 hex characters)
  - Timestamps

**What it shows:**
- How data is stored in the database
- Format of salt (binary, stored as VARBINARY)
- Format of password hash (hex string, 64 chars)
- Example of `SHA256(salt || password)` implementation

---

## How to Generate Sample Records

### Option 1: Use Existing Data
If you've registered users, export them:
```bash
mysql -u root -p securechat -e "SELECT * FROM users;" > sample_records.txt
```

### Option 2: Use the Sample File
The file `database/sample_records.sql` contains example records you can use.

### Option 3: Create Your Own
1. Register a test user in your system
2. Query the database:
```sql
SELECT id, email, username, HEX(salt) as salt_hex, pwd_hash, created_at 
FROM users;
```
3. Create INSERT statements from the results

---

## What Each File Demonstrates

### `schema.sql` Shows:
✅ Database structure  
✅ Table definition  
✅ Column types (VARBINARY for salt, CHAR(64) for hash)  
✅ Indexes for performance  
✅ Constraints (UNIQUE, NOT NULL)

### `sample_records.sql` Shows:
✅ Actual data format  
✅ Salt storage (16 bytes binary)  
✅ Password hash format (64-char hex string)  
✅ How `SHA256(salt || password)` is implemented  
✅ Real-world data examples

---

## Submission Format

Submit both files in your GitHub repository:

```
your-repo/
├── database/
│   ├── schema.sql          ← Required: Database structure
│   └── sample_records.sql  ← Required: Example data
```

**OR** combine them into one file:
```
database/
└── schema_with_samples.sql  ← Contains both schema and sample records
```

---

## Quick Check

Before submitting, verify:

- [ ] `schema.sql` creates the `users` table correctly
- [ ] `sample_records.sql` shows at least 2-3 example users
- [ ] Salt values are shown in hex format (16 bytes = 32 hex chars)
- [ ] Password hashes are 64 hex characters
- [ ] Comments explain the format

---

## Example Output

When someone runs your schema and sample records, they should see:

```sql
mysql> SELECT id, email, username, HEX(salt) as salt, pwd_hash FROM users;
+----+------------------+----------+----------------------------------+------------------------------------------------------------------+
| id | email            | username | salt                             | pwd_hash                                                         |
+----+------------------+----------+----------------------------------+------------------------------------------------------------------+
|  1 | alice@example.com| alice    | A1B2C3D4E5F6789012345678901234AB | 8F3E9A2B1C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F1A2B3 |
|  2 | bob@example.com  | bob      | F1E2D3C4B5A6978012345678901234CD | 1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F1A2B3C4D5 |
+----+------------------+----------+----------------------------------+------------------------------------------------------------------+
```

---

**That's it!** Submit both `schema.sql` and `sample_records.sql` (or combined file) in your repository. ✅

