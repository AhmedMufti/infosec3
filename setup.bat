@echo off
REM Setup script for Secure Chat System (Windows)

echo Setting up Secure Chat System...

REM Create necessary directories
if not exist certs mkdir certs
if not exist transcripts mkdir transcripts
if not exist database mkdir database

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Set up MySQL database
echo Setting up MySQL database...
echo Please run the following command manually:
echo mysql -u root -p ^< database\schema.sql

REM Generate CA and certificates
echo Generating CA and certificates...
python scripts\gen_ca.py
python scripts\gen_cert.py server
python scripts\gen_cert.py client

echo Setup complete!
echo Please configure .env file with your database credentials
echo Then run: python server.py (in one terminal)
echo And run: python client.py (in another terminal)
pause



