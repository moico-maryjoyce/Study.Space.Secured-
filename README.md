# Study.Space.Secured!
A Secure Study-Space Access & Monitoring System
Built with Python + Flet (Server-Driven UI)

## Courses Covered
- **CCCS 106 – Application Development and Emerging Technologies**
- **CS 319 – Information Assurance and Security**
- **CS 3110 – Software Engineering 1**

## Developed by: Team Rush
- Moico, Mary Joyce N.
- Oronan, Senbie
- Quite, Rona Mae M.

**BSCS - 3A**

---

# **Project Overview & Problem Statement**
Study.Space.Secured! is a secure electronic access and monitoring system aimed at shared study areas.  
It removes the use of manual logbooks through an automated, fair, and tamper-resistant system that offers:

- **Safe login and authentication**
- **Role-Based Access Control (Admin/User)**
- **Check-in/out tracking**
- **On-site activity monitoring**
- **Full audit logs for security events**

### The Problem It Solves
Conventional monitoring of study spaces is slow, easily manipulated, and lacks transparency.  
This system provides accurate time tracking, fair usage monitoring, and secure user administration.

---

# **Feature List & Scope Table**
### ✔️ In Scope
- **Authentication** (Login/Logout)  
- **RBAC**: Admin & User roles  
- **User Management** (create, lock, view)  
- **Profile Management** (name/password updates)  
- **Check-in/Check-out** with timestamps & session duration calculation  
- **Audit Logging** (login attempts, security events, admin actions)  
- **Audit Log Export** to CSV  
- **Light/Dark Theme Preference**  
- **AI-based Anomaly Detection** (simple rule-based)

### ❌ Out of Scope
- Biometric or physical access systems  
- Email verification / SMS OTP  
- Multi-venue or multi-branch deployment  
- External APIs and cloud integrations  
- Large-scale enterprise deployment

---

# **Architecture Diagram**
Below is the ERD representing the structure and relationships of the system:

![ERD Diagram](<assets/Study.Space.Secured! ERD.png>)

---

# **Database Schema (SQL)**

```sql
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
```

---

# **Emerging Tech Explanation**

### **Why Flet (Server-Driven UI)?**
- Allows a single Python codebase to deploy on **Web, Desktop, and Mobile**
- Enables **fast UI development** with automatic state synchronization
- Ideal for **security workflows** where UI must follow server logic
- Reduces complexity — **no separate frontend framework** needed

### **How It’s Integrated**
- All UI pages are served directly from Python (**SDUI architecture**)
- Buttons, tables, dialogs, themes, and navigation are **synced from the server**
- Flet handles **real-time UI updates** for check-in/out and audit logs

### **Limitations**
- Not suited for **large-scale** or **offline-first** applications
- Limited customization compared to **React** or **Flutter**
- Works on a **single-node architecture** only (no clustering)

---

# **Setup & Run Instructions**

## 1. Install Python 3.x

Verify:
```bash
python --version
```

## 2. Install Dependencies

```bash
pip install flet bcrypt
```

## 3. Run the Application

```bash
flet run main.py
```

## 4. Default Accounts (for Testing)

| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | @123 |

---

# **Testing Summary**

## How to Run Tests
If you have test scripts:
```bash
python -m pytest
```

## Coverage Notes
- Login flow tested for wrong passwords & lockout
- RBAC tested for unauthorized access
- Check-in/out correctness validated
- Audit logs tested for integrity and export
- Settings: theme persistence

---

# **Team Roles & Contribution Matrix**

| Member | Role | Contributions |
| :--- | :--- | :--- |
| **Rona Mae M. Quite** | UI/UX & Page Designer | Designed Flet pages, navigation, theme system |
| **Mary Joyce N. Moico** | Backend & Security | RBAC, bcrypt hashing, authentication logic |
| **Senbie Oronan** | Testing & Documentation | Test cases, audit log validation, writes SRS/README |

---

# **Risk / Constraint Notes & Future Enhancements**

## Risks / Constraints

* System relies on a single device/server
* No biometric verification
* Password resets are local only
* Limitations of Flet SDUI for large deployments

## Future Enhancements

* Biometric or RFID integration
* Multi-branch study space support
* More advanced anomaly detection (ML-based)
* Cloud-based backups and analytics dashboard
* Push notifications (check-in reminders)

---

# **Individual Reflection**

## Mary Joyce N. Moico

## Senbie Oronan

## Rona Mae M. Quite

My main emphasis was the development of the user interface and easy navigation with the help of the Flet library. The main dilemma was to comply with the usability specification, namely to make the procedure of the login and the check in process as fast and as user-friendly as possible. After a short time, I discovered the limitations and strengths of the Server-Driven UI (SDUI) architecture and directed my design toward the minimalistic and accessible. The name of the team Rush 3-in-1 is actually a reflection of the way the team developed, the project needed strict high-speed development to be completed on time. My task included the general page design and navigation. The project has taught me the principles of breaking down complicated security needs into clean and simple user experience, demonstrating that a powerful functionality does not need complicated graphics. The adherence to the Flet framework was effective, and thus, we were able to make the system cross-platform compatible. The high-paced development cycle eventually helped me to hone my priorities when it comes to prioritizing key UI features under stress.
















