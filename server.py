
"""
Secure Chat Server
Implements the server side of the secure chat protocol with CIANR guarantees.
"""

import os
import sys
import json
import socket
import threading
import struct
import base64
import secrets
import pymysql
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
SERVER_CERT_FILE = os.path.join(CERT_DIR, 'server_cert.pem')
SERVER_KEY_FILE = os.path.join(CERT_DIR, 'server_key.pem')
CA_CERT_FILE = os.path.join(CERT_DIR, 'ca_cert.pem')
TRANSCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'transcripts')

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'securechat')

# Server configuration
SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = int(os.getenv('SERVER_PORT', 9999))

# DH parameters (should be large primes in production)
DH_P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF
DH_G = 2


class SecureChatServer:
    """Secure Chat Server implementation."""
    
    def __init__(self):
        """Initialize the server."""
        # Load server certificate and key
        self.server_cert = crypto_utils.load_certificate(SERVER_CERT_FILE)
        self.server_key = crypto_utils.load_private_key(SERVER_KEY_FILE)
        self.ca_cert = crypto_utils.load_ca_certificate(CA_CERT_FILE)
        
        # Create transcripts directory
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        
        # Database connection
        self.db_connection = None
        self.connect_database()
        
        # Server socket
        self.server_socket = None
        self.running = False
        
    def connect_database(self):
        """Connect to MySQL database."""
        try:
            self.db_connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"Connected to database: {DB_NAME}")
        except Exception as e:
            print(f"Database connection error: {e}")
            sys.exit(1)
    
    def start(self):
        """Start the server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((SERVER_HOST, SERVER_PORT))
            self.server_socket.listen(5)
            self.running = True
            print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
            
            while self.running:
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")
                
                # Handle client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\nShutting down server...")
            self.running = False
            self.server_socket.close()
        except Exception as e:
            print(f"Server error: {e}")
            self.running = False
    
    def handle_client(self, client_socket, client_address):
        """Handle a client connection."""
        try:
            # Phase 1: Control Plane - Certificate Exchange
            client_cert = self.control_plane(client_socket)
            if not client_cert:
                return
            
            # Phase 2: Registration/Login
            user_info = self.handle_auth(client_socket, client_cert)
            if not user_info:
                return
            
            # Phase 3: Key Agreement
            session_key = self.key_agreement(client_socket)
            if not session_key:
                return
            
            # Phase 4: Data Plane - Encrypted Chat
            transcript = self.data_plane(client_socket, client_cert, session_key, user_info)
            
            # Phase 5: Non-Repudiation - Session Receipt
            self.generate_receipt(transcript, client_cert, user_info)
            
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"Client {client_address} disconnected")
    
    def control_plane(self, client_socket):
        """Handle control plane: certificate exchange and validation."""
        try:
            # Receive client hello
            data = self.receive_message(client_socket)
            if not data:
                print("Control plane: No data received from client")
                return None
            
            try:
                message = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Control plane: Invalid JSON from client: {e}")
                self.send_error(client_socket, "Invalid message format")
                return None
            
            if message.get('type') != 'hello':
                print(f"Control plane: Expected hello, got: {message.get('type')}")
                self.send_error(client_socket, "Expected hello message")
                return None
            
            # Load client certificate
            client_cert_pem = message.get('client_cert')
            if not client_cert_pem:
                print("Control plane: No client certificate in message")
                self.send_error(client_socket, "No client certificate provided")
                return None
            
            try:
                client_cert = x509.load_pem_x509_certificate(
                    client_cert_pem.encode('utf-8'),
                    default_backend()
                )
            except Exception as e:
                print(f"Control plane: Error loading client certificate: {e}")
                self.send_error(client_socket, f"Invalid client certificate: {str(e)}")
                return None
            
            # Validate client certificate
            print("Control plane: Validating client certificate...")
            is_valid, error_msg = crypto_utils.validate_certificate(client_cert, self.ca_cert)
            if not is_valid:
                print(f"Control plane: Client certificate validation failed: {error_msg}")
                self.send_error(client_socket, f"BAD CERT: {error_msg}")
                return None
            
            # Send server hello
            print("Control plane: Sending server hello...")
            server_cert_pem = self.server_cert.public_bytes(
                serialization.Encoding.PEM
            ).decode('utf-8')
            
            server_nonce = crypto_utils.generate_nonce()
            server_hello = {
                'type': 'server_hello',
                'server_cert': server_cert_pem,
                'nonce': base64.b64encode(server_nonce).decode('utf-8')
            }
            self.send_message(client_socket, server_hello)
            print("Control plane: Server hello sent")
            
            print("Control plane: Certificates exchanged and validated")
            return client_cert
            
        except Exception as e:
            print(f"Control plane error: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.send_error(client_socket, f"Control plane error: {str(e)}")
            except:
                pass
            return None
    
    def handle_auth(self, client_socket, client_cert):
        """Handle registration and login."""
        try:
            # Receive auth message (encrypted)
            data = self.receive_message(client_socket)
            if not data:
                return None
            
            message = json.loads(data)
            auth_type = message.get('type')
            
            if auth_type == 'register':
                return self.handle_register(client_socket, message, client_cert)
            elif auth_type == 'login':
                # Login may require two steps: salt request and actual login
                result = self.handle_login(client_socket, message, client_cert)
                if result is None:
                    # Salt was sent, wait for actual login message
                    data = self.receive_message(client_socket)
                    if not data:
                        return None
                    message = json.loads(data)
                    if message.get('type') == 'login':
                        return self.handle_login(client_socket, message, client_cert)
                return result
            else:
                self.send_error(client_socket, "Invalid auth type")
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def handle_register(self, client_socket, message, client_cert):
        """Handle user registration."""
        try:
            email = message.get('email')
            username = message.get('username')
            pwd_hash = message.get('pwd')  # Already hashed by client
            salt_b64 = message.get('salt')
            
            print(f"Registration attempt: email={email}, username={username}")
            
            if not all([email, username, pwd_hash, salt_b64]):
                missing = []
                if not email: missing.append('email')
                if not username: missing.append('username')
                if not pwd_hash: missing.append('pwd')
                if not salt_b64: missing.append('salt')
                error_msg = f"Missing registration fields: {', '.join(missing)}"
                print(f"Registration error: {error_msg}")
                self.send_error(client_socket, error_msg)
                return None
            
            try:
                salt = base64.b64decode(salt_b64)
            except Exception as e:
                print(f"Registration error: Invalid salt encoding: {e}")
                self.send_error(client_socket, f"Invalid salt encoding: {str(e)}")
                return None
            
            # Check if user already exists
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM users WHERE email = %s OR username = %s",
                        (email, username)
                    )
                    existing = cursor.fetchone()
                    if existing:
                        print(f"Registration error: User already exists (email={email}, username={username})")
                        self.send_error(client_socket, "User already exists")
                        return None
                    
                    # Insert new user
                    print(f"Inserting user into database...")
                    cursor.execute(
                        "INSERT INTO users (email, username, salt, pwd_hash) VALUES (%s, %s, %s, %s)",
                        (email, username, salt, pwd_hash)
                    )
                    self.db_connection.commit()
                    print(f"User inserted successfully")
            except pymysql.Error as e:
                print(f"Database error during registration: {e}")
                self.send_error(client_socket, f"Database error: {str(e)}")
                return None
            
            # Send success response
            response = {'type': 'register_success', 'message': 'Registration successful'}
            self.send_message(client_socket, response)
            
            print(f"User registered: {username} ({email})")
            return {'email': email, 'username': username}
            
        except Exception as e:
            print(f"Registration error: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(client_socket, f"Registration failed: {str(e)}")
            return None
    
    def handle_login(self, client_socket, message, client_cert):
        """Handle user login."""
        try:
            email = message.get('email')
            
            # Check if this is a salt request
            if 'pwd' not in message:
                # Client is requesting salt for login
                with self.db_connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT salt FROM users WHERE email = %s",
                        (email,)
                    )
                    user = cursor.fetchone()
                    
                    if not user:
                        self.send_error(client_socket, "User not found")
                        return None
                    
                    # Send salt to client
                    salt = user['salt']
                    response = {
                        'type': 'salt_response',
                        'salt': base64.b64encode(salt).decode('utf-8')
                    }
                    self.send_message(client_socket, response)
                    return None  # Wait for actual login message
            
            # This is the actual login message with password hash
            pwd_hash = message.get('pwd')
            nonce_b64 = message.get('nonce', '')
            
            if not all([email, pwd_hash]):
                self.send_error(client_socket, "Missing login fields")
                return None
            
            # Verify user credentials
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, salt, pwd_hash FROM users WHERE email = %s",
                    (email,)
                )
                user = cursor.fetchone()
                
                if not user:
                    self.send_error(client_socket, "Invalid credentials")
                    return None
                
                # Verify password hash (constant-time comparison)
                stored_hash = user['pwd_hash']
                if not secrets.compare_digest(pwd_hash, stored_hash):
                    self.send_error(client_socket, "Invalid credentials")
                    return None
            
            # Send success response
            response = {
                'type': 'login_success',
                'message': 'Login successful',
                'username': user['username']
            }
            self.send_message(client_socket, response)
            
            print(f"User logged in: {user['username']} ({email})")
            return {'email': email, 'username': user['username']}
            
        except Exception as e:
            print(f"Login error: {e}")
            self.send_error(client_socket, "Login failed")
            return None
    
    def key_agreement(self, client_socket):
        """Handle Diffie-Hellman key exchange."""
        try:
            # Receive DH client message
            data = self.receive_message(client_socket)
            if not data:
                return None
            
            message = json.loads(data)
            if message.get('type') != 'dh_client':
                self.send_error(client_socket, "Expected DH client message")
                return None
            
            p = message.get('p')
            g = message.get('g')
            A = message.get('A')  # Client's public value
            
            # Generate server's private key
            b = secrets.randbelow(p - 2) + 1
            B = pow(g, b, p)  # Server's public value
            
            # Send DH server message
            dh_server = {
                'type': 'dh_server',
                'B': B
            }
            self.send_message(client_socket, dh_server)
            
            # Compute shared secret
            shared_secret = pow(A, b, p)
            
            # Derive session key
            session_key = crypto_utils.derive_session_key(shared_secret)
            
            print("Key agreement: Session key established")
            return session_key
            
        except Exception as e:
            print(f"Key agreement error: {e}")
            return None
    
    def data_plane(self, client_socket, client_cert, session_key, user_info):
        """Handle encrypted message exchange."""
        transcript = []
        seqno = 0
        client_fingerprint = crypto_utils.get_certificate_fingerprint(client_cert)
        
        print("Data plane: Starting encrypted chat")
        print("Type 'quit' to end the session")
        
        try:
            while True:
                # Receive message
                data = self.receive_message(client_socket)
                if not data:
                    break
                
                message = json.loads(data)
                
                if message.get('type') == 'msg':
                    # Verify and decrypt message
                    msg_seqno = message.get('seqno')
                    timestamp = message.get('ts')
                    ciphertext_b64 = message.get('ct')
                    signature_b64 = message.get('sig')
                    
                    # Check sequence number
                    if msg_seqno <= seqno:
                        self.send_error(client_socket, "REPLAY: Invalid sequence number")
                        continue
                    seqno = msg_seqno
                    
                    # Verify signature
                    ciphertext = base64.b64decode(ciphertext_b64)
                    signature = base64.b64decode(signature_b64)
                    
                    # Compute message digest
                    digest = crypto_utils.create_message_digest(msg_seqno, timestamp, ciphertext)
                    
                    # Verify signature using client's public key
                    client_public_key = client_cert.public_key()
                    if not crypto_utils.rsa_verify(digest, signature, client_public_key):
                        self.send_error(client_socket, "SIG FAIL: Invalid signature")
                        continue
                    
                    # Decrypt message
                    try:
                        plaintext = crypto_utils.aes_decrypt(ciphertext, session_key)
                        message_text = plaintext.decode('utf-8')
                        
                        print(f"[{user_info['username']}]: {message_text}")
                        
                        # Add to transcript
                        transcript_line = f"{msg_seqno}|{timestamp}|{ciphertext_b64}|{signature_b64}|{client_fingerprint}"
                        transcript.append(transcript_line)
                        
                        # Check for quit command
                        if message_text.strip().lower() == 'quit':
                            break
                        
                    except Exception as e:
                        self.send_error(client_socket, f"Decryption error: {e}")
                        continue
                
                elif message.get('type') == 'quit':
                    break
                    
        except Exception as e:
            print(f"Data plane error: {e}")
        
        return transcript
    
    def generate_receipt(self, transcript, client_cert, user_info):
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
            signature = crypto_utils.rsa_sign(transcript_hash_bytes, self.server_key)
            signature_b64 = base64.b64encode(signature).decode('utf-8')
            
            # Create receipt
            receipt = {
                'type': 'receipt',
                'peer': 'server',
                'first_seq': first_seq,
                'last_seq': last_seq,
                'transcript_sha256': transcript_hash,
                'sig': signature_b64
            }
            
            # Save transcript and receipt
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            transcript_file = os.path.join(
                TRANSCRIPTS_DIR,
                f"server_{user_info['username']}_{timestamp}.txt"
            )
            
            with open(transcript_file, 'w') as f:
                f.write('\n'.join(transcript))
                f.write('\n--- RECEIPT ---\n')
                f.write(json.dumps(receipt, indent=2))
            
            print(f"Session receipt generated: {transcript_file}")
            
        except Exception as e:
            print(f"Receipt generation error: {e}")
    
    def send_message(self, socket, message):
        """Send a JSON message to the client."""
        try:
            data = json.dumps(message).encode('utf-8')
            # Send message length first
            length = len(data)
            socket.sendall(struct.pack('>I', length))
            # Send message data
            socket.sendall(data)
        except Exception as e:
            print(f"Send message error: {e}")
    
    def receive_message(self, socket):
        """Receive a JSON message from the client."""
        try:
            # Receive message length
            length_data = self.recv_all(socket, 4)
            if not length_data:
                return None
            length = struct.unpack('>I', length_data)[0]
            
            # Receive message data
            data = self.recv_all(socket, length)
            if not data:
                return None
            
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive message error: {e}")
            return None
    
    def recv_all(self, socket, n):
        """Receive exactly n bytes."""
        data = b''
        while len(data) < n:
            chunk = socket.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data
    
    def send_error(self, socket, error_message):
        """Send an error message to the client."""
        error = {'type': 'error', 'message': error_message}
        self.send_message(socket, error)


def main():
    """Main function."""
    server = SecureChatServer()
    server.start()


if __name__ == '__main__':
    main()

