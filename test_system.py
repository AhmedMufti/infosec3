#!/usr/bin/env python3
"""
Test script to demonstrate the secure chat system.
This script will generate certificates and show the system working.
"""

import os
import sys
import subprocess

def run_command(cmd, input_text=None):
    """Run a command and return output."""
    try:
        if input_text:
            result = subprocess.run(
                cmd,
                shell=True,
                input=input_text,
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("=" * 60)
    print("Secure Chat System - Test and Demonstration")
    print("=" * 60)
    print()
    
    # Check if certificates exist
    cert_dir = "certs"
    ca_cert = os.path.join(cert_dir, "ca_cert.pem")
    ca_key = os.path.join(cert_dir, "ca_key.pem")
    server_cert = os.path.join(cert_dir, "server_cert.pem")
    server_key = os.path.join(cert_dir, "server_key.pem")
    client_cert = os.path.join(cert_dir, "client_cert.pem")
    client_key = os.path.join(cert_dir, "client_key.pem")
    
    print("Step 1: Checking certificates...")
    if os.path.exists(ca_cert) and os.path.exists(ca_key):
        print("✓ CA certificate and key exist")
    else:
        print("✗ CA certificate not found. Generating...")
        success, stdout, stderr = run_command("python scripts\\gen_ca.py", input_text="y\n")
        if success:
            print("✓ CA generated successfully")
            print(stdout)
        else:
            print("✗ Failed to generate CA")
            print(stderr)
            return
    
    if os.path.exists(server_cert) and os.path.exists(server_key):
        print("✓ Server certificate and key exist")
    else:
        print("✗ Server certificate not found. Generating...")
        success, stdout, stderr = run_command("python scripts\\gen_cert.py server")
        if success:
            print("✓ Server certificate generated successfully")
            print(stdout)
        else:
            print("✗ Failed to generate server certificate")
            print(stderr)
    
    if os.path.exists(client_cert) and os.path.exists(client_key):
        print("✓ Client certificate and key exist")
    else:
        print("✗ Client certificate not found. Generating...")
        success, stdout, stderr = run_command("python scripts\\gen_cert.py client")
        if success:
            print("✓ Client certificate generated successfully")
            print(stdout)
        else:
            print("✗ Failed to generate client certificate")
            print(stderr)
    
    print()
    print("Step 2: Verifying certificate files...")
    cert_files = [
        ("CA Certificate", ca_cert),
        ("CA Key", ca_key),
        ("Server Certificate", server_cert),
        ("Server Key", server_key),
        ("Client Certificate", client_cert),
        ("Client Key", client_key)
    ]
    
    all_exist = True
    for name, path in cert_files:
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✓ {name}: {path} ({size} bytes)")
        else:
            print(f"✗ {name}: {path} (NOT FOUND)")
            all_exist = False
    
    if not all_exist:
        print("\n⚠ Some certificates are missing. Please generate them manually:")
        print("  python scripts\\gen_ca.py")
        print("  python scripts\\gen_cert.py server")
        print("  python scripts\\gen_cert.py client")
        return
    
    print()
    print("Step 3: Checking Python modules...")
    try:
        import cryptography
        print(f"✓ cryptography module installed (version: {cryptography.__version__})")
    except ImportError:
        print("✗ cryptography module not found")
        return
    
    try:
        import pymysql
        print(f"✓ pymysql module installed")
    except ImportError:
        print("⚠ pymysql module not found (needed for database)")
    
    try:
        import dotenv
        print(f"✓ python-dotenv module installed")
    except ImportError:
        print("⚠ python-dotenv module not found")
    
    print()
    print("Step 4: Testing cryptographic utilities...")
    try:
        import crypto_utils
        print("✓ crypto_utils module loaded successfully")
        
        # Test hash function
        test_data = b"test data"
        hash_result = crypto_utils.compute_hash(test_data)
        print(f"✓ SHA-256 hash function works: {hash_result.hex()[:16]}...")
        
        # Test nonce generation
        nonce = crypto_utils.generate_nonce()
        print(f"✓ Nonce generation works: {len(nonce)} bytes")
        
    except Exception as e:
        print(f"✗ Error testing crypto_utils: {e}")
        return
    
    print()
    print("=" * 60)
    print("System Status: READY")
    print("=" * 60)
    print()
    print("To run the system:")
    print("1. Set up MySQL database: mysql -u root -p < database\\schema.sql")
    print("2. Configure .env file with database credentials")
    print("3. Start server: python server.py")
    print("4. Start client: python client.py")
    print()
    print("Note: The system requires MySQL to be running for full functionality.")
    print("Certificates are ready and cryptographic functions are working.")

if __name__ == '__main__':
    main()

