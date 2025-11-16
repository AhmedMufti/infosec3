@echo off
echo ========================================
echo Secure Chat System - Running
echo ========================================
echo.

echo Step 1: Installing dependencies...
python -m pip install cryptography pymysql python-dotenv
echo.

echo Step 2: Testing cryptography...
python -c "import cryptography; print('Cryptography installed successfully')"
if errorlevel 1 (
    echo ERROR: Cryptography not installed. Please install manually.
    pause
    exit /b 1
)
echo.

echo Step 3: Generating certificates...
echo Generating CA...
echo y | python scripts\gen_ca.py
echo.
echo Generating server certificate...
echo y | python scripts\gen_cert.py server
echo.
echo Generating client certificate...
echo y | python scripts\gen_cert.py client
echo.

echo Step 4: Certificates generated!
echo.
echo To run the system:
echo   1. Set up MySQL database: mysql -u root -p ^< database\schema.sql
echo   2. Create .env file with database credentials
echo   3. Start server: python server.py
echo   4. Start client: python client.py
echo.
pause

