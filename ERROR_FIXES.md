# Error Fixes Applied

## Issues Found and Fixed

### 1. CryptographyDeprecationWarning ✅ FIXED
**Error:**
```
CryptographyDeprecationWarning: Properties that return a naïve datetime object have been deprecated. 
Please switch to not_valid_before_utc.
```

**Fix Applied:**
- Updated `crypto_utils.py` to use `not_valid_before_utc` and `not_valid_after_utc` instead of deprecated methods
- Added fallback for older cryptography versions

**Location:** `crypto_utils.py` lines 57-68

### 2. Protocol Error: "Expected server_hello message" ✅ FIXED
**Error:**
- Client sends hello but doesn't receive server_hello
- Connection gets closed by server

**Root Cause:**
- Certificate validation was failing silently
- Server wasn't sending proper error messages
- Exception handling wasn't comprehensive

**Fixes Applied:**
1. **Better Error Handling in Server:**
   - Added detailed logging at each step
   - Added try-catch around certificate loading
   - Added JSON parsing error handling
   - Server now always sends a response (either server_hello or error)

2. **Better Error Handling in Client:**
   - Added error message detection
   - Better JSON parsing error handling
   - More informative error messages

3. **Certificate Signature Verification:**
   - Fixed signature algorithm detection
   - Properly maps OID to hash algorithm
   - Better error messages for signature failures

**Locations:**
- `server.py` lines 148-212 (control_plane method)
- `client.py` lines 119-138 (control_plane method)
- `crypto_utils.py` lines 70-102 (validate_certificate method)

## Testing the Fixes

After these fixes, you should see:

1. **No more deprecation warnings** - Certificate date validation uses UTC-aware methods
2. **Better error messages** - If certificate validation fails, you'll see exactly why
3. **Proper protocol flow** - Server always responds, either with server_hello or an error message

## Next Steps

1. **Regenerate certificates** (if needed):
   ```bash
   python scripts/gen_ca.py
   python scripts/gen_cert.py server
   python scripts/gen_cert.py client
   ```

2. **Run the system again:**
   ```bash
   # Terminal 1
   python server.py
   
   # Terminal 2
   python client.py
   ```

3. **Check the output:**
   - Server should show: "Control plane: Validating client certificate..."
   - Server should show: "Control plane: Sending server hello..."
   - Client should receive server_hello and proceed

## If Issues Persist

If you still see errors, check:
1. Are certificates generated? (Check `certs/` directory)
2. Are certificates valid? (Check expiry dates)
3. Are certificates signed by the same CA?
4. Check server logs for detailed error messages

The improved error handling will now show exactly what's failing.

