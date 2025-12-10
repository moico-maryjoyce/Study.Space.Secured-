-- ================================
-- Database Schema
-- System: Study Space Secured
-- DBMS: MySQL (XAMPP)
-- Frontend: Flet
-- ================================

CREATE DATABASE IF NOT EXISTS study_space_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE study_space_db;

-- ================================
-- USERS TABLE
-- ================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ================================
-- CHECK-IN LOGS TABLE
-- ================================
CREATE TABLE checkin_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    checkin_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(255),
    device VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ================================
-- ACTIVITY LOGS TABLE
-- ================================
CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    description TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ================================
-- AUDIT LOGS TABLE (ADMIN)
-- ================================
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    target VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id)
        ON DELETE CASCADE
);

-- ================================
-- SAMPLE DATA (OPTIONAL)
-- ================================
INSERT INTO users (username, email, password_hash, role)
VALUES
('admin', 'admin@system.com', 'admin', 'adminadmin'),
('student1', 'student1@test.com', 'user', 'useruser');
