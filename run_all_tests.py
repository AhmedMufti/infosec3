#!/usr/bin/env python3
"""
Run All Security Tests
This script runs all required tests for the assignment.
"""
import os
import sys
import subprocess
import time

print("=" * 70)
print("SECURE CHAT SYSTEM - COMPREHENSIVE TEST SUITE")
print("=" * 70)
print()

tests = [
    ("Certificate Validation", "test_cert_validation.py"),
    ("Database Setup", "test_db.py"),
    ("Invalid Certificate Test", "test_invalid_cert.py"),
    ("Tampering Detection Test", "test_tampering.py"),
    ("Replay Attack Test", "test_replay.py"),
    ("Non-Repudiation Test", "test_non_repudiation.py"),
]

print("Running tests...")
print()

results = []
for test_name, test_file in tests:
    print(f"{'=' * 70}")
    print(f"TEST: {test_name}")
    print(f"{'=' * 70}")
    print()
    
    if os.path.exists(test_file):
        try:
            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            if result.returncode == 0:
                results.append((test_name, "PASSED"))
                print(f"✓ {test_name}: PASSED")
            else:
                results.append((test_name, "FAILED"))
                print(f"✗ {test_name}: FAILED")
        except Exception as e:
            results.append((test_name, f"ERROR: {e}"))
            print(f"✗ {test_name}: ERROR - {e}")
    else:
        results.append((test_name, "FILE NOT FOUND"))
        print(f"✗ {test_name}: Test file not found")
    
    print()
    time.sleep(1)

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print()
for test_name, status in results:
    status_symbol = "[PASS]" if status == "PASSED" else "[FAIL]"
    print(f"{status_symbol} {test_name}: {status}")
print()
print("=" * 70)

