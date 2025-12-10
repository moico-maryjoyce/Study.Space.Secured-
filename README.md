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
| **Senbie Oronan** | UI/UX & Page Designer | Designed Flet pages, navigation, theme system |
| **Mary Joyce N. Moico** | Backend & Security | RBAC, bcrypt hashing, authentication logic |
| **Rona Mae M. Quite** | Testing & Documentation | Test cases, audit log validation, writes SRS/README |

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
The development of Study.Space.Secured! was a difficult but at the same time a very rewarding experience that granted our team the opportunity to use and mix concepts from Application Development, Software Engineering, and Information Assurance into one working system. Even though the time was limited, we persevered as a team and were able to provide an application for study-space access and monitoring that was secure and based on Python and Flet. We also learnt that the project had four major components: planning, teamwork, security-aware design. The features that we implemented - role-based access control, authentication, audit logging, and check-in/check-out tracking, were all together us to better appreciate the fact that real-world systems must weigh the trade-off between usability and security. Using Flet’s server-driven UI also helped us to see how the use of emerging technologies can ease development while still allowing control over the critical workflows. But more than anything else, this project was a testament to the power of collaboration. Each of the contributors brought in their strengths, and even though time was a factor, we still provided support to one another to have the system completed. Our team name, Team Rush 3-in-1, actually summarized our journey very well, fast working, combining ideas into one system, and delivering as one team. Study.Space.Secured! is a demonstration that when there is teamwork, dedication, and a shared responsibility, even quality outputs in a short period are possible.

## Senbie Oronan

## Rona Mae M. Quite
It was important that I played a key role in making the Study.Space.Secured! system verifiable, reliable as well as well-documented. This included the creation of all the test cases, validation of the non-functional requirements, and writing of Sz S, the Software Requirements Specification, and the README. The name of the team, in fact, Rush 3-in-1, accurately represents how we were developing it since we had to do the testing and documentation in a high-speed and focused way in order to meet our deadlines. One of the priorities was to verify the integrity of the Audit Log and the performance, and the complex queries should be returned in less than 2 seconds. To make sure the code base was progressing towards the aggressive goal of unit test coverage of at least 70 percent and to ensure our CI tests ran fast, I needed to make sure the code base was moving along. The project has also helped me to learn that testing and documentation are not only a conclusion but the necessary means of implementing security policies (such as the login lockout) and ensuring the overall quality and maintainability of the system in the future.
















