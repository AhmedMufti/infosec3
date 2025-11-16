# Database Schema and Sample Records - Brief Explanation

## What It Means

### Schema Dump
**Definition:** The SQL file that creates your database structure (tables, columns, indexes, etc.)

**What it contains:**
- `CREATE DATABASE` statement
- `CREATE TABLE` statements
- Column definitions (name, type, constraints)
- Indexes for performance

**File:** `database/schema.sql`

### Sample Records
**Definition:** Example data showing what actual user records look like in your database

**What it contains:**
- `INSERT` statements with example users
- Real salt values (16 bytes, shown as hex)
- Real password hashes (SHA256, 64 hex characters)
- Shows how `SHA256(salt || password)` is stored

**File:** `database/sample_records.sql`

---

## Files to Submit

Submit these **2 files** in your GitHub repository:

```
database/
├── schema.sql          ← Database structure (tables, columns)
└── sample_records.sql  ← Example data (sample users)
```

---

## Quick Summary

| Item | What It Is | File |
|------|------------|------|
| **Schema** | Database structure (how tables are created) | `database/schema.sql` |
| **Sample Records** | Example data (what actual records look like) | `database/sample_records.sql` |

---

## Why Both Are Needed

- **Schema** shows the **structure** (what columns exist, their types)
- **Sample Records** show the **data format** (how salt and hash are actually stored)

Together, they prove:
✅ You have a proper database structure  
✅ You're storing passwords correctly (salted + hashed)  
✅ The format matches the requirement: `SHA256(salt || password)`

---

**That's it!** Just submit both files in your `database/` folder. ✅

