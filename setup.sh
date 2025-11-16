#!/bin/bash
# Setup script for Secure Chat System

echo "Setting up Secure Chat System..."

# Create necessary directories
mkdir -p certs transcripts database

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up MySQL database
echo "Setting up MySQL database..."
echo "Please enter your MySQL root password:"
read -s MYSQL_PASSWORD
mysql -u root -p$MYSQL_PASSWORD < database/schema.sql

# Generate CA and certificates
echo "Generating CA and certificates..."
python scripts/gen_ca.py
python scripts/gen_cert.py server
python scripts/gen_cert.py client

echo "Setup complete!"
echo "Please configure .env file with your database credentials"
echo "Then run: python server.py (in one terminal)"
echo "And run: python client.py (in another terminal)"



