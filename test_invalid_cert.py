
"""
Test: Invalid Certificate Rejection
This test verifies that the server rejects invalid/expired/self-signed certificates.
"""
import os
import sys
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta, timezone

def create_invalid_cert():
    """Create an invalid (self-signed) certificate for testing."""
    print("=" * 70)
    print("TEST: Invalid Certificate Rejection")
    print("=" * 70)
    print()
    
    # Generate a self-signed certificate (should be rejected)
    print("Creating invalid self-signed certificate...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PK"),
        x509.NameAttribute(NameOID.COMMON_NAME, "Invalid-Cert"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(timezone.utc)
    ).not_valid_after(
        datetime.now(timezone.utc) + timedelta(days=365)
    ).sign(private_key, hashes.SHA256(), default_backend())
    
    # Save invalid cert
    invalid_cert_path = "certs/invalid_cert.pem"
    with open(invalid_cert_path, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"[OK] Invalid certificate saved to {invalid_cert_path}")
    print()
    print("This certificate is self-signed and should be rejected by the server.")
    print()
    print("To test:")
    print("1. Replace client_cert.pem with invalid_cert.pem temporarily")
    print("2. Try to connect with client.py")
    print("3. Server should respond with: BAD CERT: Self-signed certificate rejected")
    print()
    print("=" * 70)

if __name__ == '__main__':
    create_invalid_cert()

