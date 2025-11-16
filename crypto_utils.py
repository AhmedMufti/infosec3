"""
Cryptographic Utilities Module
Provides functions for certificate validation, encryption, signing, and key exchange.
"""

import os
import hashlib
import base64
import struct
from datetime import datetime
from cryptography import x509
from cryptography.x509 import oid as x509_oid
from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import secrets


def load_certificate(cert_path):
    """Load an X.509 certificate from a PEM file."""
    with open(cert_path, 'rb') as f:
        cert_data = f.read()
        return x509.load_pem_x509_certificate(cert_data, default_backend())


def load_private_key(key_path):
    """Load a private key from a PEM file."""
    with open(key_path, 'rb') as f:
        key_data = f.read()
        return serialization.load_pem_private_key(
            key_data,
            password=None,
            backend=default_backend()
        )


def load_ca_certificate(ca_cert_path):
    """Load the CA certificate."""
    return load_certificate(ca_cert_path)


def validate_certificate(cert, ca_cert):
    """
    Validate a certificate against a CA certificate.
    
    Args:
        cert: The certificate to validate
        ca_cert: The CA certificate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check if certificate is expired
        # Use UTC-aware datetime for comparison
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        # Use UTC-aware datetime methods to avoid deprecation warnings
        if hasattr(cert, 'not_valid_before_utc'):
            if cert.not_valid_before_utc > now:
                return False, "Certificate not yet valid"
            if cert.not_valid_after_utc < now:
                return False, "Certificate expired"
        else:
            # Fallback for older versions - convert to timezone-aware
            not_before = cert.not_valid_before
            not_after = cert.not_valid_after
            # Make timezone-aware if needed
            if not_before.tzinfo is None:
                not_before = not_before.replace(tzinfo=timezone.utc)
            if not_after.tzinfo is None:
                not_after = not_after.replace(tzinfo=timezone.utc)
            
            if not_before > now:
                return False, "Certificate not yet valid"
            if not_after < now:
                return False, "Certificate expired"
        
        # Verify certificate signature
        try:
            # Get the signature algorithm from the certificate
            sig_algorithm = cert.signature_algorithm_oid
            hash_algorithm = None
            
            # Map OID to hash algorithm
            if sig_algorithm == x509_oid.SignatureAlgorithmOID.RSA_WITH_MD5:
                hash_algorithm = hashes.MD5()
            elif sig_algorithm == x509_oid.SignatureAlgorithmOID.RSA_WITH_SHA1:
                hash_algorithm = hashes.SHA1()
            elif sig_algorithm == x509_oid.SignatureAlgorithmOID.RSA_WITH_SHA256:
                hash_algorithm = hashes.SHA256()
            elif sig_algorithm == x509_oid.SignatureAlgorithmOID.RSA_WITH_SHA384:
                hash_algorithm = hashes.SHA384()
            elif sig_algorithm == x509_oid.SignatureAlgorithmOID.RSA_WITH_SHA512:
                hash_algorithm = hashes.SHA512()
            else:
                # Default to SHA256
                hash_algorithm = hashes.SHA256()
            
            # Verify signature
            ca_cert.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                asym_padding.PKCS1v15(),
                hash_algorithm
            )
        except InvalidSignature:
            return False, "Invalid certificate signature"
        except Exception as e:
            return False, f"Certificate signature verification error: {str(e)}"
        
        # Check if certificate is self-signed (should not be trusted)
        if cert.subject == cert.issuer:
            return False, "Self-signed certificate rejected"
        
        # Verify issuer matches CA
        if cert.issuer != ca_cert.subject:
            return False, "Certificate issuer does not match CA"
        
        # Check Basic Constraints
        try:
            basic_constraints = cert.extensions.get_extension_for_oid(
                x509.oid.ExtensionOID.BASIC_CONSTRAINTS
            ).value
            if basic_constraints.ca:
                return False, "Certificate has CA flag set"
        except x509.ExtensionNotFound:
            pass
        
        return True, "Certificate valid"
        
    except Exception as e:
        return False, f"Certificate validation error: {str(e)}"


def get_certificate_fingerprint(cert):
    """Get SHA-256 fingerprint of a certificate."""
    fingerprint = hashlib.sha256(cert.public_bytes(serialization.Encoding.DER)).digest()
    return fingerprint.hex()


def generate_nonce(size=16):
    """Generate a random nonce."""
    return secrets.token_bytes(size)


def derive_session_key(shared_secret):
    """
    Derive AES-128 session key from Diffie-Hellman shared secret.
    
    Args:
        shared_secret: The shared secret (integer)
        
    Returns:
        bytes: 16-byte AES key
    """
    # Convert shared secret to big-endian bytes
    # Use a fixed size to ensure consistent key derivation
    secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, 'big')
    
    # Compute SHA-256 hash
    hash_obj = hashlib.sha256(secret_bytes)
    hash_digest = hash_obj.digest()
    
    # Truncate to 16 bytes for AES-128
    return hash_digest[:16]


def aes_encrypt(plaintext, key):
    """
    Encrypt plaintext using AES-128 with PKCS#7 padding.
    
    Args:
        plaintext: Plaintext bytes to encrypt
        key: 16-byte AES key
        
    Returns:
        bytes: Ciphertext
    """
    # PKCS#7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext)
    padded_data += padder.finalize()
    
    # Generate random IV
    iv = secrets.token_bytes(16)
    
    # Encrypt with AES-128 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return IV + ciphertext
    return iv + ciphertext


def aes_decrypt(ciphertext, key):
    """
    Decrypt ciphertext using AES-128 with PKCS#7 unpadding.
    
    Args:
        ciphertext: Ciphertext bytes (IV + encrypted data)
        key: 16-byte AES key
        
    Returns:
        bytes: Plaintext
    """
    # Extract IV and encrypted data
    iv = ciphertext[:16]
    encrypted_data = ciphertext[16:]
    
    # Decrypt with AES-128 in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Remove PKCS#7 padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext)
    plaintext += unpadder.finalize()
    
    return plaintext


def compute_hash(data):
    """Compute SHA-256 hash of data."""
    return hashlib.sha256(data).digest()


def rsa_sign(data, private_key):
    """
    Sign data using RSA private key.
    
    Args:
        data: Data to sign (bytes)
        private_key: RSA private key
        
    Returns:
        bytes: Signature
    """
    # Compute SHA-256 hash
    hash_obj = hashlib.sha256(data)
    
    # Sign the hash
    signature = private_key.sign(
        hash_obj.digest(),
        asym_padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    return signature


def rsa_verify(data, signature, public_key):
    """
    Verify RSA signature.
    
    Args:
        data: Original data (bytes)
        signature: Signature to verify (bytes)
        public_key: RSA public key
        
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Compute SHA-256 hash
        hash_obj = hashlib.sha256(data)
        
        # Verify signature
        public_key.verify(
            signature,
            hash_obj.digest(),
            asym_padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


def create_message_digest(seqno, timestamp, ciphertext):
    """
    Create message digest for signing.
    
    Args:
        seqno: Sequence number (int)
        timestamp: Timestamp in milliseconds (int)
        ciphertext: Ciphertext bytes
        
    Returns:
        bytes: Digest bytes
    """
    # Convert seqno and timestamp to bytes
    seqno_bytes = seqno.to_bytes(8, 'big')
    ts_bytes = timestamp.to_bytes(8, 'big')
    
    # Concatenate: seqno || timestamp || ciphertext
    data = seqno_bytes + ts_bytes + ciphertext
    
    # Compute SHA-256 hash
    return compute_hash(data)


def hash_password(password, salt):
    """
    Hash password with salt using SHA-256.
    
    Args:
        password: Plaintext password (str)
        salt: Salt bytes
        
    Returns:
        str: Hex-encoded hash
    """
    # Concatenate salt and password
    data = salt + password.encode('utf-8')
    
    # Compute SHA-256 hash
    hash_obj = hashlib.sha256(data)
    return hash_obj.hexdigest()


def generate_salt(size=16):
    """Generate a random salt."""
    return secrets.token_bytes(size)


def compute_transcript_hash(transcript_lines):
    """
    Compute hash of session transcript.
    
    Args:
        transcript_lines: List of transcript lines (strings)
        
    Returns:
        str: Hex-encoded hash
    """
    # Concatenate all transcript lines
    transcript_data = '\n'.join(transcript_lines).encode('utf-8')
    
    # Compute SHA-256 hash
    hash_obj = hashlib.sha256(transcript_data)
    return hash_obj.hexdigest()


def get_timestamp_ms():
    """Get current timestamp in milliseconds."""
    return int(datetime.utcnow().timestamp() * 1000)



