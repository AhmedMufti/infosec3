import sys
import os

# Test imports
print("Testing imports...")
try:
    from cryptography import x509
    print("✓ cryptography module works")
except Exception as e:
    print(f"✗ cryptography: {e}")
    sys.exit(1)

# Try to generate CA
print("\nGenerating CA...")
try:
    from scripts.gen_ca import create_ca
    # Monkey patch input to auto-answer
    import builtins
    _original_input = builtins.input
    builtins.input = lambda prompt: "y"
    
    create_ca()
    
    builtins.input = _original_input
    print("✓ CA generated successfully")
except Exception as e:
    print(f"✗ CA generation failed: {e}")
    import traceback
    traceback.print_exc()

# Try to generate server cert
print("\nGenerating server certificate...")
try:
    from scripts.gen_cert import create_certificate
    import builtins
    _original_input = builtins.input
    builtins.input = lambda prompt: "y"
    
    create_certificate("server", "server")
    
    builtins.input = _original_input
    print("✓ Server certificate generated successfully")
except Exception as e:
    print(f"✗ Server cert generation failed: {e}")

# Try to generate client cert
print("\nGenerating client certificate...")
try:
    from scripts.gen_cert import create_certificate
    import builtins
    _original_input = builtins.input
    builtins.input = lambda prompt: "y"
    
    create_certificate("client", "client")
    
    builtins.input = _original_input
    print("✓ Client certificate generated successfully")
except Exception as e:
    print(f"✗ Client cert generation failed: {e}")

print("\n" + "="*60)
print("Certificate generation complete!")
print("="*60)

