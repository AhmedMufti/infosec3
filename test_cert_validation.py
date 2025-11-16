#!/usr/bin/env python3
"""Test certificate validation fix"""
import os
import sys

try:
    from crypto_utils import load_certificate, validate_certificate, load_ca_certificate
    
    print("Testing certificate validation...")
    print("-" * 70)
    
    # Check if certificates exist
    ca_cert_path = "certs/ca_cert.pem"
    client_cert_path = "certs/client_cert.pem"
    
    if not os.path.exists(ca_cert_path):
        print("[FAIL] CA certificate not found")
        print("  Run: python scripts/gen_ca.py")
        sys.exit(1)
    
    if not os.path.exists(client_cert_path):
        print("[FAIL] Client certificate not found")
        print("  Run: python scripts/gen_cert.py client")
        sys.exit(1)
    
    # Load certificates
    print("Loading certificates...")
    ca_cert = load_ca_certificate(ca_cert_path)
    client_cert = load_certificate(client_cert_path)
    
    print("[OK] CA certificate loaded")
    print("[OK] Client certificate loaded")
    
    # Test validation
    print("\nValidating client certificate...")
    is_valid, error_msg = validate_certificate(client_cert, ca_cert)
    
    if is_valid:
        print("[OK] Certificate validation: SUCCESS")
        print(f"  Message: {error_msg}")
    else:
        print("[FAIL] Certificate validation: FAILED")
        print(f"  Error: {error_msg}")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("Certificate validation test: PASSED")
    print("=" * 70)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

