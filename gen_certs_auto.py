#!/usr/bin/env python3
"""Auto-generate certificates without user input"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import the CA generation function
from scripts.gen_ca import create_ca
from scripts.gen_cert import create_certificate

# Generate CA
print("=" * 60)
print("Generating CA...")
print("=" * 60)
try:
    create_ca()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Generate server certificate
print("\n" + "=" * 60)
print("Generating Server Certificate...")
print("=" * 60)
try:
    create_certificate("server", "server")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Generate client certificate
print("\n" + "=" * 60)
print("Generating Client Certificate...")
print("=" * 60)
try:
    create_certificate("client", "client")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All certificates generated successfully!")
print("=" * 60)

