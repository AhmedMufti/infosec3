#!/usr/bin/env python3
"""
Certificate Generation Script
Issues RSA X.509 certificates for server and client, signed by the root CA.
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

# Certificate Configuration from environment
CA_COUNTRY = os.getenv('CA_COUNTRY', 'PK')
CA_STATE = os.getenv('CA_STATE', 'State')
CA_LOCALITY = os.getenv('CA_LOCALITY', 'City')
CA_ORG = os.getenv('CA_ORG', 'FAST-NUCES')
CA_ORG_UNIT = os.getenv('CA_ORG_UNIT', 'CS')
CERT_VALIDITY_DAYS = int(os.getenv('CERT_VALIDITY_DAYS', '365'))


def load_ca():
    """Load CA private key and certificate."""
    if not os.path.exists(CA_KEY_FILE) or not os.path.exists(CA_CERT_FILE):
        raise FileNotFoundError("CA not found. Please run gen_ca.py first.")
    
    # Load CA private key
    with open(CA_KEY_FILE, 'rb') as f:
        ca_private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )
    
    # Load CA certificate
    with open(CA_CERT_FILE, 'rb') as f:
        ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())
    
    return ca_private_key, ca_cert


def create_certificate(entity_name, entity_type):
    """
    Create a certificate for the given entity (server or client).
    
    Args:
        entity_name: Name of the entity (e.g., 'server', 'client')
        entity_type: Type of entity ('server' or 'client')
    """
    # Load CA
    ca_private_key, ca_cert = load_ca()
    
    # Generate entity private key
    print(f"Generating {entity_name} private key...")
    entity_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Certificate file paths
    key_file = os.path.join(CERT_DIR, f'{entity_name}_key.pem')
    cert_file = os.path.join(CERT_DIR, f'{entity_name}_cert.pem')
    
    # Check if certificate already exists
    if os.path.exists(key_file) and os.path.exists(cert_file):
        print(f"Certificate for {entity_name} already exists.")
        response = input("Do you want to regenerate? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
        os.remove(key_file)
        os.remove(cert_file)
    
    # Create certificate subject
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, CA_COUNTRY),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, CA_STATE),
        x509.NameAttribute(NameOID.LOCALITY_NAME, CA_LOCALITY),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, CA_ORG),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, CA_ORG_UNIT),
        x509.NameAttribute(NameOID.COMMON_NAME, entity_name),
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, f'{entity_name}@securechat.local'),
    ])
    
    # Create certificate
    print(f"Generating {entity_name} certificate...")
    cert_builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        entity_private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=CERT_VALIDITY_DAYS)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    )
    
    # Add key usage based on entity type
    if entity_type == 'server':
        cert_builder = cert_builder.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.ExtendedKeyUsageOID.SERVER_AUTH,
            ]),
            critical=True,
        )
    else:  # client
        cert_builder = cert_builder.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                content_commitment=False,
                data_encipherment=False,
                encipher_only=False,
                decipher_only=False
            ),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage([
                x509.ExtendedKeyUsageOID.CLIENT_AUTH,
            ]),
            critical=True,
        )
    
    # Add Subject Alternative Name (SAN) for server
    if entity_type == 'server':
        cert_builder = cert_builder.add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName('localhost'),
                x509.DNSName('127.0.0.1'),
            ]),
            critical=False,
        )
    
    # Sign certificate with CA private key
    cert = cert_builder.sign(ca_private_key, hashes.SHA256(), default_backend())
    
    # Save entity private key
    with open(key_file, 'wb') as f:
        f.write(entity_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"{entity_name} private key saved to {key_file}")
    
    # Save entity certificate
    with open(cert_file, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"{entity_name} certificate saved to {cert_file}")
    
    # Display certificate information
    print(f"\n{entity_name.upper()} Certificate Information:")
    print(f"  Subject: {subject}")
    print(f"  Issuer: {ca_cert.subject}")
    print(f"  Serial Number: {cert.serial_number}")
    print(f"  Valid From: {cert.not_valid_before}")
    print(f"  Valid To: {cert.not_valid_after}")
    print(f"  Key Size: 2048 bits")
    print(f"\n{entity_name.upper()} certificate created successfully!")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python gen_cert.py <server|client>")
        sys.exit(1)
    
    entity_type = sys.argv[1].lower()
    if entity_type not in ['server', 'client']:
        print("Error: Entity type must be 'server' or 'client'")
        sys.exit(1)
    
    try:
        create_certificate(entity_type, entity_type)
    except Exception as e:
        print(f"Error creating certificate: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()



