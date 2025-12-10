# Study.Space.Secured!
A Secure Study-Space Access & Monitoring System
Built with Python + Flet (Server-Driven UI)

## Courses Covered
- **CCCS 106 – Application Development and Emerging Technologies**
- **CS 319 – Information Assurance and Security**
- **CS 3110 – Software Engineering 1**

## Developed by: Team Rush 3-in-1
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

# **Visual Preview**

## Admin View (Management & Monitoring)
This view provides exclusive access to user management and security features.

![Start Screen](<assets/Start Screen.png>)
![Login](<assets/Log In.png>)
![Dashboard](<assets/Dashboard - Admin.png>)
![Check InOut](<assets/Check InOut.png>)
![My Profile](<assets/My Profile.png>)
![User](<assets/User Management.png>)
![Audit Logs](<assets/Audit Logs.png>)
![Settings](<assets/Settings.png>)

## User View
This view focuses on the user's core functions: logging in, creating acc, check-in/out, and personal settings.

![Start Screen](<assets/Start Screen.png>)
![Login](<assets/Log In.png>)
![Create Acc](<assets/Create Acc Page.png>)
![Dashboard](<assets/Dashboard - User.png>)
![Check InOut](<assets/Check InOut - User.png>)
![My Profile](<assets/My Profile - User.png>)
![Settings](<assets/Settings.png>)

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
The backend was a hard one
Debugging made it even harder. But what's worse is leaving behind the team and letting the others cram the work, one thing I'll never forget. Checking the UI, system security, and revising everything in just 15 minutes is not good.  Whoever reads this may think it is not even connected to the system. But it is, one thing that makes the system work smoothly is teamwork and proper communication. 

This system, Study,.Space.Secured! is built for a peer tracking mainly but then switching it to a more useful one where it shows how a community flows. Where some went alone to study, some with a group and there is someone doing the tracking and guiding.  The same goes with the system. System parts may never be the same and lots of trial and error but still meet in the middle. Where, at the end once the errors debugged it works beyond what you just imagined.

## Rona Mae M. Quite
In this project, I had a significant role to play in ensuring that Study.Space.Secured! was not only operational but also verifiable, reliable and well documented. I did the design of the test cases, tested the non-functional requirements and prepared significant documents such as the Software Requirements Specification and the README. The name of our team, Rush 3-in-1, definitely reflected our working style; we were precise, efficient, and determined to perform good in the end despite the tight timeline.

Enhance the integrity and the performance of the Audit Log, particularly, the ability of complex queries to be returned in less than two seconds, was one of the most important activities I chose to focus on. I was also involved in ensuring that the code base was kept under continuous improvement towards our desired 70+ unit test coverage and ensuring that our CI tests were running smoothly. This project made me understand that testing and documentation are not only the end tasks but the necessary ones to perform security measures such as lockout of a system after a user logs into it and the long-term quality and maintainability of the system.
















