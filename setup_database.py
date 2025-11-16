#!/usr/bin/env python3
"""Setup database table automatically"""
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
print("Database Setup")
print("=" * 70)
print()

print(f"Database: {DB_NAME}")
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
    print("✓ Connected to database")
    
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ 'users' table already exists")
            response = input("Do you want to recreate it? (y/n): ")
            if response.lower() == 'y':
                cursor.execute("DROP TABLE users")
                print("  Dropped existing table")
            else:
                print("  Keeping existing table")
                connection.close()
                sys.exit(0)
        
        # Create table
        print("\nCreating 'users' table...")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL UNIQUE,
            salt VARBINARY(16) NOT NULL,
            pwd_hash CHAR(64) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_email (email),
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        cursor.execute(create_table_sql)
        connection.commit()
        print("✓ Table created successfully")
        
        # Verify table structure
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print("\nTable structure:")
        for col in columns:
            print(f"  - {col['Field']}: {col['Type']}")
    
    connection.close()
    print()
    print("=" * 70)
    print("Database setup complete!")
    print("=" * 70)
    
except pymysql.Error as e:
    print(f"✗ Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

