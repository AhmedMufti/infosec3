-- Secure Chat Database Schema
-- MySQL Database for User Management

CREATE DATABASE IF NOT EXISTS securechat;
USE securechat;

-- Users table for storing user credentials
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    salt VARBINARY(16) NOT NULL,
    pwd_hash CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data (for testing only - remove in production)
-- Password: testpass123
-- Salt: (randomly generated)
-- pwd_hash: SHA256(salt || password) in hex format



