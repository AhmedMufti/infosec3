#!/usr/bin/env python3
"""
Secure Chat Client
Implements the client side of the secure chat protocol with CIANR guarantees.
"""

import os
import sys
import json
import socket
import struct
import base64
import secrets
from datetime import datetime
from dotenv import load_dotenv
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import crypto_utils

# Load environment variables
load_dotenv()

# Configuration
CERT_DIR = os.path.join(os.path.dirname(__file__), 'certs')
CLIENT_CERT_FILE = os.path.join(CERT_DIR, 'client_cert.pem')
CLIENT_KEY_FILE = os.path.join(CERT_DIR, 'client_key.pem')
CA_CERT_FILE = os.path.join(CERT_DIR, 'ca_cert.pem')
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'transcripts')

# Server configuration
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 9999))

# DH parameters (must match server)
DH_P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF
DH_G = 2


class SecureChatClient:
    """Secure Chat Client implementation."""
    
    def __init__(self):
        """Initialize the client."""
        # Load client certificate and key
        self.client_cert = crypto_utils.load_certificate(CLIENT_CERT_FILE)
        self.client_key = crypto_utils.load_private_key(CLIENT_KEY_FILE)
        self.ca_cert = crypto_utils.load_ca_certificate(CA_CERT_FILE)
        
        # Create transcripts directory
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        
        # Client socket
        self.client_socket = None
        self.server_cert = None
        self.session_key = None
        self.seqno = 0
        self.user_info = None
        
    def connect(self):
        """Connect to the server."""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def start(self):
        """Start the client and handle protocol phases."""
        if not self.connect():
            return
        
        try:
            # Phase 1: Control Plane - Certificate Exchange
            if not self.control_plane():
                return
            
            # Phase 2: Registration/Login
            if not self.handle_auth():
                return
            
            # Phase 3: Key Agreement
            if not self.key_agreement():
                return
            
            # Phase 4: Data Plane - Encrypted Chat
            transcript = self.data_plane()
            
            # Phase 5: Non-Repudiation - Session Receipt
            self.generate_receipt(transcript)
            
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            if self.client_socket:
                self.client_socket.close()
    
    def control_plane(self):
        """Handle control plane: certificate exchange and validation."""
        try:
            # Send client hello
            client_cert_pem = self.client_cert.public_bytes(
                serialization.Encoding.PEM
            ).decode('utf-8')
            
            client_nonce = crypto_utils.generate_nonce()
            client_hello = {
                'type': 'hello',
                'client_cert': client_cert_pem,
                'nonce': base64.b64encode(client_nonce).decode('utf-8')
            }
            self.send_message(client_hello)
            
            # Receive server hello
            data = self.receive_message()
            if not data:
                print("Error: No response from server")
                return False
            
            try:
                message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON response from server: {data[:100]}")
                return False
            
            if message.get('type') == 'error':
                print(f"Error from server: {message.get('message', 'Unknown error')}")
                return False
            
            if message.get('type') != 'server_hello':
                print(f"Error: Expected server_hello message, got: {message.get('type')}")
                print(f"Message: {message}")
                return False
            
            # Load server certificate
            server_cert_pem = message.get('server_cert')
            if not server_cert_pem:
                print("Error: No server certificate provided")
                return False
            
            self.server_cert = x509.load_pem_x509_certificate(
                server_cert_pem.encode('utf-8'),
                default_backend()
            )
            
            # Validate server certificate
            is_valid, error_msg = crypto_utils.validate_certificate(self.server_cert, self.ca_cert)
            if not is_valid:
                print(f"Error: BAD CERT: {error_msg}")
                return False
            
            print("Control plane: Certificates exchanged and validated")
            return True
            
        except Exception as e:
            print(f"Control plane error: {e}")
            return False
    
    def handle_auth(self):
        """Handle registration and login."""
        try:
            # Ask user for action
            print("\n1. Register")
            print("2. Login")
            choice = input("Enter choice (1/2): ").strip()
            
            if choice == '1':
                return self.handle_register()
            elif choice == '2':
                return self.handle_login()
            else:
                print("Invalid choice")
                return False
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def handle_register(self):
        """Handle user registration."""
        try:
            email = input("Email: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            # Generate salt
            salt = crypto_utils.generate_salt()
            
            # Hash password
            pwd_hash = crypto_utils.hash_password(password, salt)
            
            # Create registration message
            register_msg = {
                'type': 'register',
                'email': email,
                'username': username,
                'pwd': pwd_hash,
                'salt': base64.b64encode(salt).decode('utf-8')
            }
            
            # Send registration message (not encrypted in initial version)
            # In full implementation, this should be encrypted with temporary DH key
            self.send_message(register_msg)
            
            # Receive response
            data = self.receive_message()
            if not data:
                return False
            
            response = json.loads(data)
            if response.get('type') == 'register_success':
                print("Registration successful!")
                self.user_info = {'email': email, 'username': username}
                return True
            elif response.get('type') == 'error':
                error_msg = response.get('message', 'Unknown error')
                print(f"Registration failed: {error_msg}")
                return False
            else:
                print(f"Unexpected response: {response}")
                return False
                
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    def handle_login(self):
        """Handle user login."""
        try:
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            # Step 1: Request salt from server
            salt_request = {
                'type': 'login',
                'email': email
            }
            self.send_message(salt_request)
            
            # Receive salt response
            data = self.receive_message()
            if not data:
                return False
            
            response = json.loads(data)
            if response.get('type') == 'error':
                print(f"Login failed: {response.get('message')}")
                return False
            elif response.get('type') != 'salt_response':
                print("Unexpected response")
                return False
            
            # Get salt from server
            salt_b64 = response.get('salt')
            if not salt_b64:
                print("Error: No salt received")
                return False
            
            salt = base64.b64decode(salt_b64)
            
            # Step 2: Compute password hash and send login message
            pwd_hash = crypto_utils.hash_password(password, salt)
            nonce = crypto_utils.generate_nonce()
            
            login_msg = {
                'type': 'login',
                'email': email,
                'pwd': pwd_hash,
                'nonce': base64.b64encode(nonce).decode('utf-8')
            }
            
            self.send_message(login_msg)
            
            # Receive login response
            data = self.receive_message()
            if not data:
                return False
            
            response = json.loads(data)
            if response.get('type') == 'login_success':
                print("Login successful!")
                # Get username from server response if available
                username = response.get('username', email.split('@')[0])
                self.user_info = {'email': email, 'username': username}
                return True
            elif response.get('type') == 'error':
                print(f"Login failed: {response.get('message')}")
                return False
            else:
                print("Unexpected response")
                return False
                
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def key_agreement(self):
        """Handle Diffie-Hellman key exchange."""
        try:
            # Generate client's private key
            a = secrets.randbelow(DH_P - 2) + 1
            A = pow(DH_G, a, DH_P)  # Client's public value
            
            # Send DH client message
            dh_client = {
                'type': 'dh_client',
                'g': DH_G,
                'p': DH_P,
                'A': A
            }
            self.send_message(dh_client)
            
            # Receive DH server message
            data = self.receive_message()
            if not data:
                return False
            
            message = json.loads(data)
            if message.get('type') != 'dh_server':
                print("Error: Expected DH server message")
                return False
            
            B = message.get('B')  # Server's public value
            
            # Compute shared secret
            shared_secret = pow(B, a, DH_P)
            
            # Derive session key
            self.session_key = crypto_utils.derive_session_key(shared_secret)
            
            print("Key agreement: Session key established")
            return True
            
        except Exception as e:
            print(f"Key agreement error: {e}")
            return False
    
    def data_plane(self):
        """Handle encrypted message exchange."""
        transcript = []
        server_fingerprint = crypto_utils.get_certificate_fingerprint(self.server_cert)
        
        print("\nData plane: Starting encrypted chat")
        print("Type messages and press Enter to send")
        print("Type 'quit' to end the session\n")
        
        try:
            # Start message receiving thread
            import threading
            receive_thread = threading.Thread(target=self.receive_messages, args=(transcript, server_fingerprint))
            receive_thread.daemon = True
            receive_thread.start()
            
            # Send messages
            while True:
                message_text = input()
                
                if message_text.strip().lower() == 'quit':
                    # Send quit message
                    quit_msg = {'type': 'quit'}
                    self.send_message(quit_msg)
                    break
                
                # Encrypt and send message
                self.send_encrypted_message(message_text, transcript, server_fingerprint)
                
        except Exception as e:
            print(f"Data plane error: {e}")
        
        return transcript
    
    def send_encrypted_message(self, plaintext, transcript, server_fingerprint):
        """Send an encrypted message."""
        try:
            # Increment sequence number
            self.seqno += 1
            
            # Get timestamp
            timestamp = crypto_utils.get_timestamp_ms()
            
            # Encrypt message
            plaintext_bytes = plaintext.encode('utf-8')
            ciphertext = crypto_utils.aes_encrypt(plaintext_bytes, self.session_key)
            ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
            
            # Create message digest
            digest = crypto_utils.create_message_digest(self.seqno, timestamp, ciphertext)
            
            # Sign digest
            signature = crypto_utils.rsa_sign(digest, self.client_key)
            signature_b64 = base64.b64encode(signature).decode('utf-8')
            
            # Create message
            message = {
                'type': 'msg',
                'seqno': self.seqno,
                'ts': timestamp,
                'ct': ciphertext_b64,
                'sig': signature_b64
            }
            
            # Send message
            self.send_message(message)
            
            # Add to transcript
            transcript_line = f"{self.seqno}|{timestamp}|{ciphertext_b64}|{signature_b64}|{server_fingerprint}"
            transcript.append(transcript_line)
            
        except Exception as e:
            print(f"Send message error: {e}")
    
    def receive_messages(self, transcript, server_fingerprint):
        """Receive and decrypt messages from server."""
        try:
            while True:
                data = self.receive_message()
                if not data:
                    break
                
                message = json.loads(data)
                
                if message.get('type') == 'msg':
                    # Verify and decrypt message
                    msg_seqno = message.get('seqno')
                    timestamp = message.get('ts')
                    ciphertext_b64 = message.get('ct')
                    signature_b64 = message.get('sig')
                    
                    # Verify signature
                    ciphertext = base64.b64decode(ciphertext_b64)
                    signature = base64.b64decode(signature_b64)
                    
                    # Compute message digest
                    digest = crypto_utils.create_message_digest(msg_seqno, timestamp, ciphertext)
                    
                    # Verify signature using server's public key
                    server_public_key = self.server_cert.public_key()
                    if not crypto_utils.rsa_verify(digest, signature, server_public_key):
                        print("Error: SIG FAIL: Invalid signature")
                        continue
                    
                    # Decrypt message
                    try:
                        plaintext = crypto_utils.aes_decrypt(ciphertext, self.session_key)
                        message_text = plaintext.decode('utf-8')
                        
                        print(f"[Server]: {message_text}")
                        
                        # Add to transcript
                        transcript_line = f"{msg_seqno}|{timestamp}|{ciphertext_b64}|{signature_b64}|{server_fingerprint}"
                        transcript.append(transcript_line)
                        
                    except Exception as e:
                        print(f"Decryption error: {e}")
                        continue
                
                elif message.get('type') == 'error':
                    print(f"Error: {message.get('message')}")
                
        except Exception as e:
            print(f"Receive messages error: {e}")
    
    def generate_receipt(self, transcript):
        """Generate session receipt for non-repudiation."""
        try:
            if not transcript:
                return
            
            # Compute transcript hash
            transcript_hash = crypto_utils.compute_transcript_hash(transcript)
            
            # Get first and last sequence numbers
            first_seq = int(transcript[0].split('|')[0])
            last_seq = int(transcript[-1].split('|')[0])
            
            # Sign transcript hash
            transcript_hash_bytes = bytes.fromhex(transcript_hash)
            signature = crypto_utils.rsa_sign(transcript_hash_bytes, self.client_key)
            signature_b64 = base64.b64encode(signature).decode('utf-8')
            
            # Create receipt
            receipt = {
                'type': 'receipt',
                'peer': 'client',
                'first_seq': first_seq,
                'last_seq': last_seq,
                'transcript_sha256': transcript_hash,
                'sig': signature_b64
            }
            
            # Save transcript and receipt
            if self.user_info:
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                transcript_file = os.path.join(
                    TRANSCRIPTS_DIR,
                    f"client_{self.user_info['username']}_{timestamp}.txt"
                )
                
                with open(transcript_file, 'w') as f:
                    f.write('\n'.join(transcript))
                    f.write('\n--- RECEIPT ---\n')
                    f.write(json.dumps(receipt, indent=2))
                
                print(f"\nSession receipt generated: {transcript_file}")
            
        except Exception as e:
            print(f"Receipt generation error: {e}")
    
    def send_message(self, message):
        """Send a JSON message to the server."""
        try:
            data = json.dumps(message).encode('utf-8')
            # Send message length first
            length = len(data)
            self.client_socket.sendall(struct.pack('>I', length))
            # Send message data
            self.client_socket.sendall(data)
        except Exception as e:
            print(f"Send message error: {e}")
    
    def receive_message(self):
        """Receive a JSON message from the server."""
        try:
            # Receive message length
            length_data = self.recv_all(4)
            if not length_data:
                return None
            length = struct.unpack('>I', length_data)[0]
            
            # Receive message data
            data = self.recv_all(length)
            if not data:
                return None
            
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive message error: {e}")
            return None
    
    def recv_all(self, n):
        """Receive exactly n bytes."""
        data = b''
        while len(data) < n:
            chunk = self.client_socket.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data


def main():
    """Main function."""
    client = SecureChatClient()
    client.start()


if __name__ == '__main__':
    main()

