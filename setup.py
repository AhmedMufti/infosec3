#!/usr/bin/env python3
"""
Setup script for Secure Chat System
Automates the setup process including dependencies, database, and certificates.
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("=" * 70)
    print("Secure Chat System - Setup")
    print("=" * 70)
    print()
    
    # Create necessary directories
    print("Creating directories...")
    directories = ['certs', 'transcripts', 'database']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  [OK] {directory}/")
    
    # Install Python dependencies
    print("\n" + "=" * 70)
    print("Step 1: Installing Python dependencies...")
    print("=" * 70)
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Warning: Some dependencies may not have installed correctly.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Database setup
    print("\n" + "=" * 70)
    print("Step 2: Database Setup")
    print("=" * 70)
    print("Please set up MySQL database manually:")
    print("  1. Make sure MySQL is running")
    print("  2. Run: mysql -u root -p < database/schema.sql")
    print("  OR use: python setup_database.py")
    print()
    print("Note: You can set up the database later using: python setup_database.py")
    print()
    
    # Generate CA and certificates
    print("\n" + "=" * 70)
    print("Step 3: Generating Certificates")
    print("=" * 70)
    
    # Check if certificates already exist
    cert_files = [
        'certs/ca_cert.pem',
        'certs/server_cert.pem',
        'certs/client_cert.pem'
    ]
    
    certs_exist = all(os.path.exists(f) for f in cert_files)
    
    if certs_exist:
        print("Certificates already exist.")
        print("Skipping certificate generation.")
        print("To regenerate, delete certs/ directory and run this script again.")
    else:
        # Generate certificates
        print("Generating certificates...")
        
        # Generate CA
        if not run_command("python scripts/gen_ca.py", "Generating CA"):
            print("Error generating CA. Please check the error above.")
            sys.exit(1)
        
        # Generate server certificate
        if not run_command("python scripts/gen_cert.py server", "Generating server certificate"):
            print("Error generating server certificate. Please check the error above.")
            sys.exit(1)
        
        # Generate client certificate
        if not run_command("python scripts/gen_cert.py client", "Generating client certificate"):
            print("Error generating client certificate. Please check the error above.")
            sys.exit(1)
    
    # Final instructions
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Create .env file with your database credentials:")
    print("     DB_HOST=localhost")
    print("     DB_PORT=3306")
    print("     DB_USER=root")
    print("     DB_PASSWORD=your_password")
    print("     DB_NAME=securechat")
    print("     SERVER_HOST=localhost")
    print("     SERVER_PORT=9999")
    print()
    print("  2. Start the server:")
    print("     python server.py")
    print()
    print("  3. In another terminal, start the client:")
    print("     python client.py")
    print()
    print("  4. Run tests:")
    print("     python run_all_tests.py")
    print()
    print("=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

