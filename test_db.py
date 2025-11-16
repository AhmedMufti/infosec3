#!/usr/bin/env python3
"""Test database connection and setup"""
import os
import sys
from dotenv import load_dotenv
import pymysql

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'securechat')

print("=" * 70)
print("Database Connection Test")
print("=" * 70)
print()

print(f"Connecting to database:")
print(f"  Host: {DB_HOST}")
print(f"  Port: {DB_PORT}")
print(f"  User: {DB_USER}")
print(f"  Database: {DB_NAME}")
print()

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✓ Database connection successful!")
    print()
    
    # Check if users table exists
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'users'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ 'users' table exists")
            
            # Check table structure
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            print("\nTable structure:")
            for col in columns:
                print(f"  - {col['Field']}: {col['Type']}")
            
            # Check if table is empty
            cursor.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()
            print(f"\nCurrent users in database: {count['count']}")
        else:
            print("✗ 'users' table does NOT exist")
            print("  Run: mysql -u root -p < database/schema.sql")
    
    connection.close()
    print()
    print("=" * 70)
    print("Database test: PASSED")
    print("=" * 70)
    
except pymysql.Error as e:
    print(f"✗ Database error: {e}")
    print()
    print("Possible issues:")
    print("  1. MySQL server is not running")
    print("  2. Database 'securechat' does not exist")
    print("  3. Wrong credentials in .env file")
    print("  4. User table not created")
    print()
    print("To fix:")
    print("  1. Start MySQL server")
    print("  2. Create database: CREATE DATABASE securechat;")
    print("  3. Run schema: mysql -u root -p < database/schema.sql")
    print("  4. Check .env file credentials")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

