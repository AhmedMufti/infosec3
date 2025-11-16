#!/usr/bin/env python3
"""
Certificate Authority (CA) Generation Script
Creates a root CA by generating a private key and a self-signed certificate.
"""

import os
import sys
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CERT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'certs')
CA_KEY_FILE = os.path.join(CERT_DIR, 'ca_key.pem')
CA_CERT_FILE = os.path.join(CERT_DIR, 'ca_cert.pem')

# CA Configuration from environment
CA_COUNTRY = os.getenv('CA_COUNTRY', 'PK')
CA_STATE = os.getenv('CA_STATE', 'State')
CA_LOCALITY = os.getenv('CA_LOCALITY', 'City')
CA_ORG = os.getenv('CA_ORG', 'FAST-NUCES')
CA_ORG_UNIT = os.getenv('CA_ORG_UNIT', 'CS')
CA_COMMON_NAME = os.getenv('CA_COMMON_NAME', 'SecureChat-CA')
CA_EMAIL = os.getenv('CA_EMAIL', 'ca@securechat.local')
CA_VALIDITY_DAYS = int(os.getenv('CA_VALIDITY_DAYS', '3650'))


def create_ca():
    """Create a root Certificate Authority."""
    # Create certs directory if it doesn't exist
    os.makedirs(CERT_DIR, exist_ok=True)
    
    # Check if CA already exists
    if os.path.exists(CA_KEY_FILE) and os.path.exists(CA_CERT_FILE):
        print(f"CA already exists at {CERT_DIR}")
        response = input("Do you want to regenerate? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
        os.remove(CA_KEY_FILE)
        os.remove(CA_CERT_FILE)
    
    print("Generating CA private key...")
    # Generate CA private key (2048 bits RSA)
    ca_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Save CA private key
    with open(CA_KEY_FILE, 'wb') as f:
        f.write(ca_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"CA private key saved to {CA_KEY_FILE}")
    
    # Create CA certificate
    print("Generating CA certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, CA_COUNTRY),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, CA_STATE),
        x509.NameAttribute(NameOID.LOCALITY_NAME, CA_LOCALITY),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, CA_ORG),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, CA_ORG_UNIT),
        x509.NameAttribute(NameOID.COMMON_NAME, CA_COMMON_NAME),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, CA_EMAIL),
    ])
    
    ca_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        ca_private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=CA_VALIDITY_DAYS)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).add_extension(
        x509.KeyUsage(
            key_cert_sign=True,
            crl_sign=True,
            digital_signature=True,
            key_encipherment=False,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False
        ),
        critical=True,
    ).sign(ca_private_key, hashes.SHA256(), default_backend())
    
    # Save CA certificate
    with open(CA_CERT_FILE, 'wb') as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
    print(f"CA certificate saved to {CA_CERT_FILE}")
    
    # Display certificate information
    print("\nCA Certificate Information:")
    print(f"  Subject: {subject}")
    print(f"  Serial Number: {ca_cert.serial_number}")
    print(f"  Valid From: {ca_cert.not_valid_before}")
    print(f"  Valid To: {ca_cert.not_valid_after}")
    print(f"  Key Size: 2048 bits")
    print("\nCA created successfully!")


if __name__ == '__main__':
    try:
        create_ca()
    except Exception as e:
        print(f"Error creating CA: {e}", file=sys.stderr)
        sys.exit(1)



