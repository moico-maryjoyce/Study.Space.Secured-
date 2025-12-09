# **Course:** APPLICATION DEVELOPMENT AND EMERGING TECHNOLOGIES (CCCS 106)  
### **Joint Collaboration:** CS 3110 – Software Engineering (Team Process & Engineering Practices)  
### **Project Title:** *Emerging Tech Flet Framework*  
### **Assessment Type:** Project & Final Examination Equivalent  
### **Term:** AY 2025–2026 (Finals)

---
# **Project Overview & Problem Statement**

## **Project Name**
**Study.Space.Secured!**

---

## **Project Overview**
**Study.Space.Secured!** is a unified, secure digital access system built using the **Flet framework** and **Server-Driven UI (SDUI)** architecture. Its primary objective is to streamline and digitize the security and entry processes in a shared study space. The system aims to ensure fairness, accuracy, and efficiency through strong security policies and a transparent workflow for different user roles.

---

## **Problem Statement**
Shared academic facilities need an auditable and secure access management method—something not achievable through manual sign-in sheets. The core issue addressed by this application is the lack of an effective, transparent, and secure access control system for a common study area.

The system solves this through:

### **1. Enforcing Security**
- Strong authentication  
- Advanced password policies  
- Login lockouts  

### **2. Granting Access**
- Admin role: User Management  
- User role: Check-in / Check-out  

### **3. Tracking History**
- Records all security-sensitive events in a tamper-resistant audit log  
- Detects anomalies using basic AI intelligence  

# **Feature List & Scope Table**

The project followed an **Agile/Scrum 2-day sprint model**, completing all baseline requirements and integrating key enhancements defined in the SRS.

---

## **1. Implemented Features (Baseline & Enhancements)**

| **Category**              | **Feature Name**          | **Description & Status** |
|---------------------------|----------------------------|---------------------------|
| **Authentication & Core** | Secure Login/Logout        | Mandatory login with credentials. |
|                           | Account Lockout Policy     | 5 unsuccessful attempts → 15-minute lockout (FR-001). |
|                           | Session Timeout            | Auto-logout after 15 minutes of inactivity (FR-001). |
| **User Role (Student)**   | Check-in/out               | Records user presence, timestamps, and session duration (FR-004). |
|                           | Profile Management         | Users can edit profile and change passwords with enforced policy (FR-003). |
| **Admin Role**            | User Management (CRUD)     | Add, update, delete, lock/unlock users (FR-002). |
|                           | Audit Log Viewer/Export    | View, filter, and export logs to CSV (FR-005). |
| **Security Enhancements** | Advanced Password Policy   | Complexity rules (≥10 chars, special char) + 3-history reuse check (FR-003). |
|                           | 2FA (OTP) Simulation       | Optional 6-digit OTP-based Two-Factor Authentication (FR-003). |
| **Emerging Tech**         | AI-Assisted Security       | Detects and flags anomalous login behavior (FR-005). |

**Export to Sheets** ✓

---

## **2. Scope Definition (What's In vs. What's Out)**

| **Area**        | **In Scope**                                                                 | **Out of Scope** |
|------------------|------------------------------------------------------------------------------|------------------|
| **Functionality** | Authentication, RBAC, User Management, Profile Management, Check-in/out tracking, Audit Logging. | Biometrics, actual email systems, complex scheduling. |
| **Deployment**    | Flet cross-platform support (Web, Desktop, PWA).                            | Large-scale deployment, external APIs, 3rd-party services. |
| **Security**      | Lockout, Session Timeout, Password Hashing, AI Anomaly Detection.           | Live IP/location tracking, advanced security protocols (e.g., certificate pinning). |
| **Data**          | SQLite persistence, structured JSON schema (mock ERD).                      | Full SQLAlchemy setup, complex DB migrations. |

---

# **Architecture Diagram & Data Model**

---

## **Architecture Diagram**  
*(Simple block-style representation with Flet, Data Layer, and Emerging Tech Layer)*

# **Emerging Tech Explanation**

## **Technology:**  
### **AI-Assisted Security Anomaly Detection (FR-005)**  

The emerging technology integrated into **Study.Space.Secured!** is a custom, statistical AI logic for **Behavioral Anomaly Detection**. This elevates system security from simple static credential checks to dynamic, data-driven behavioral analysis.

---

## **Why This Technology Was Chosen**

### **1. Detective Control**
It functions as a **Detective Security Control**, identifying potential threats that may bypass traditional authentication (e.g., an attacker possessing a valid password).

### **2. Advisory Function**
Instead of automatically applying punitive actions, the system **flags anomalous behavior** for review.  
This addresses **False Positive Risk (R-003)** and maintains system reliability and usability.

### **3. Curriculum Relevance**
The feature demonstrates the integration of **basic machine learning concepts** such as statistical profiling within a Python-based Flet application, fulfilling the *Emerging Technologies* requirement.

---

## **How It Is Integrated**

The anomaly detection logic runs in the **backend**, woven directly into the authentication and activity logging workflow.

### **Data Source**
- Uses the **ActivityLog**, which stores all login attempts and successful sessions.  
- Builds a personalized historical profile for each user.

### **Profiling**
- On each login, the system reviews past login patterns (primarily **time** and **frequency**) to establish normal behavior.

### **Anomaly Checks**
The system evaluates two key conditions:

1. **Temporal Outlier**  
   - Login occurs at a significantly unusual time compared to the user's prior sessions.

2. **Velocity Spike**  
   - Login follows a sudden cluster of failed attempts or happens immediately after a lockout window, indicating potential brute-force activity.

### **Action**
- If the login event is deemed suspicious:
  - The Audit Log entry is marked with `is_suspicious = true`
  - This allows Admins to inspect the event without disrupting user access.

---

## **Limitations**

### **Advisory Only**
- The detection system only flags events; it does **not** automatically lock accounts to avoid false positives.

### **Statistical (Not ML-Heavy)**
- The model is a **simple statistical analyzer**, not a self-learning neural network or deep learning system.

### **Data Scope Limits**
- No tracking of IP address or live geolocation.  
- Relies strictly on **time-based** and **frequency-based** behavioral patterns.  
- Reference: *Rush3-in-1_SRS*.

---
# **Setup & Run Instructions**

---

## **1. Prerequisites and Dependencies**

The system is built on a modern Python stack and requires only one primary library for execution.

| **Prerequisite** | **Version** | **Justification** |
|------------------|-------------|--------------------|
| **Python**       | 3.10 or higher | Required for Flet backend logic. |
| **Flet**         | Latest stable version | Core framework for cross-platform UI and SDUI architecture. |

---
## **2. Dependency Installation**

Install **Flet** using pip:

```bash
pip install flet
```

This command installs all essential dependencies required to run the **Study.Space.Secured!** application.

---

## **3. Running the Application**

Follow these steps to launch **Study.Space.Secured!**:

### **Step 1: Navigate to the Project Directory**
```bash
cd views_updated/
```
## 3. Running the Application

Follow these steps to launch **Study.Space.Secured!**:

### **Step 1: Navigate to the Project Directory**
```bash
cd views_updated/
```

## 4. Default Credentials (for Testing)

Use the following credentials to test the Role-Based Access Control (RBAC) features:

| Role        | Username  | Password                                          |
|-------------|-----------|--------------------------------------------------|
| Admin       | admin     | Refer to `users.json` for the hashed value       |
| User        | john_doe  | Refer to `users.json` for the hashed value       |


---

## 5. Platform Targets

The system is designed for broad cross-platform compatibility:

- **Web Application** – Runs directly in any modern web browser.  
- **Standalone Desktop** – Can be packaged as a single executable for Windows, macOS, and Linux.  
- **Mobile** – Can be deployed as a Progressive Web App (PWA) or accessed through the Flet mobile client.  

# Testing Summary

The testing process for **Study.Space.Secured!** focused on verifying that all functional and non-functional requirements, particularly the critical security controls, are testable and meet defined performance targets.

---

## 1. Testing Methodology

**Approach:**  
Testing was conducted manually following an **Acceptance Test-Driven Development (ATDD)** principle, where the outcome of every feature was checked against the criteria defined in the project's User Stories.  

**Test Focus:**  
The testing prioritized **security** and **performance** requirements:

- **Security Controls:**  
  - Verifying the integrity of the **Audit Log**  
  - Functionality of the **Lockout Policy** (5 failed attempts → 15 min lock)  
  - Correct **RBAC** enforcement  

- **Performance:**  
  - Ensuring **user login** completes in ≤ 1 second  
  - Ensuring **profile updates** complete in ≤ 1.5 seconds  

---

## 2. How to Execute Test Suite (Manual Verification)

Since the core focus was on manual verification of security features, running the "test suite" involves manually executing specific sequences in the Flet application:

1. **Run Application:**  
   Launch the app using:  
   ```bash
   flet run main.py
   ```
## Verify Lockout
- Use a test account to intentionally fail login **5 times**  
- Verify the account locks on the **6th attempt**  
- Confirm the event is logged in the **Audit Log**

## Verify RBAC
- Log in as a **regular User**  
- Verify that the **Users** and **Audit Logs** navigation tabs are correctly hidden (Least Privilege)

## Verify Anomaly Detection
- Manually trigger a suspicious login (e.g., login immediately after a simulated lockout timeout)  
- Check the **Audit Log Viewer** to confirm that the event is flagged as an **Anomaly**

## 3. Coverage Notes & Targets

| Metric                        | Target                                           | Status                                                                       |
|-------------------------------|-------------------------------------------------|-----------------------------------------------------------------------------|
| **Unit Test Coverage**         | ≥ 70% of codebase                               | Focus established on core modules (`auth.py`, `activity_log.py`)            |
| **Testability (Requirement Quality)** | Every requirement must be verifiable with clear input/process/output | Achieved by mapping all FRs to testable actions                              |
| **Performance (Login Time)**   | User login ≤ 1 second                           | Confirmed successful in manual tests due to efficient Python core/Flet design|

# Team Roles & Contribution Matrix

This matrix outlines the primary responsibilities and contributions of each team member during the two-day agile sprint, reflecting the specialized skill areas required to complete the **Study.Space.Secured!** project.

| Team Member        | Primary Role                  | Key Modules & Contributions                                                                                       |
|-------------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------|
| [Member 1 Name]    | UI/UX & Flet Page Designer    | - Implemented core Flet pages (Login, Dashboard, Profile, Admin Views) and navigation structure  <br> - Responsible for front-end validation and NFR-002 (Usability) |
| [Member 2 Name]    | Backend & Database Lead       | - Defined the JSON data schema (mocking ERD)  <br> - Implemented User CRUD logic and the transactional Check-in/out flow  <br> - Implemented core RBAC enforcement |
| [Member 3 Name]    | Security & Emerging Tech Specialist | - Implemented Lockout/Timeout policies (FR-001)  <br> - Developed the Audit Log (FR-005) viewer, filtering, and export  <br> - Integrated the AI Anomaly Detector logic (FR-005) |

# Risk / Constraint Notes & Future Enhancements

## 1. Constraints and Dependencies

Constraints are factors that limit the design and implementation of the system.

| Type               | Description                                                                                   | Mitigation/Note                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| **Technical Stack** | Development must use Python 3.x with the Flet library.                                         | Enforces a single-stack, cross-platform architecture (NFR-005).                                   |
| **Data Persistence** | The system must use SQLAlchemy connected to a local SQLite file.                             | Limits initial scalability, but ensures data integrity via WAL mode (NFR-004).                   |
| **Security Parameters** | Password hashing must use bcrypt (≥12 cost factor), and Lockout (5 failed attempts) and Timeout (15 min) values are fixed. | These policies are non-negotiable security requirements.                                         |
| **Functionality**   | The OTP functionality is a simulation; no actual external email infrastructure is integrated. | This is a dependency limitation for the mini-scope.                                              |

---

## 2. Risk Notes (Adapted from Risk Register)

| Risk ID | Description                                             | Mitigation Plan                                                                                       |
|---------|---------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| R-001   | Weak Password Policies or Compromised Credentials.     | Implemented a strict password policy (min 10 chars, special chars), bcrypt hashing (simulated), Lockout, and Audit Logging. |
| R-002   | Improper Shutdown causing SQLite Data Corruption.      | Production system must operate in WAL mode and maintain regular backups (NFR-004).                 |
| R-003   | AI Anomaly Detection resulting in False Positives.     | Anomaly flags are strictly advisory (Detective Control); they log the event but do not automatically block the user, requiring Admin review. |

---

## 3. Future Enhancements

These are features planned for the next development iteration:

- **Full Relational Database Migration:** Complete integration with SQLAlchemy/SQLite (or full MySQL connection), moving away from file-based JSON persistence.  
- **Real-Time 2FA Integration:** Upgrade the simulated OTP functionality to integrate with a live external email or SMS service.  
- **Real-time Admin Dashboard:** Implement live Flet updates to show current check-in status without manual refreshing, improving data visualization performance.  
- **Configuration File Management:** Externalize key variables (Lockout time, Timeout duration, etc.) into a central configuration file for easy modification (NFR-006).  

## Individual Reflection (Per Member)

## 1. [Member 1 Name]'s Reflection: UI/UX & Flet Page Designer
"My primary contribution was translating the security requirements into a clean, intuitive, and cross-platform user interface. The most significant success was mastering the Flet framework to implement the Server-Driven UI (SDUI), which allowed us to rapidly deploy the application on desktop and web targets. A key learning curve was ensuring the dynamic nature of Flet pages correctly implemented the Role-Based Access Control (RBAC), specifically making sure Admin features like the User Management table were conditionally rendered. I focused intensely on NFR-002 (Usability), ensuring that complex actions, like the check-in/out feature, could be completed in minimal clicks. Moving forward, I am confident in Flet's potential but recognize that managing complex component state still demands deep understanding of the framework's reactive model. The speed of Flet was essential to delivering the full scope within the compressed two-day sprint."

---

## 2. [Member 2 Name]'s Reflection: Backend & Database Lead
"My responsibility was to build the secure foundation, focusing on data integrity and user access control logic. The initial challenge was designing the data access layer (users_data.py) to correctly mock the SQLAlchemy/SQLite schema while maintaining speed. My greatest success was implementing the robust RBAC and Authentication pipeline (auth.py). This involved writing the logic to simulate secure password hashing, enforcing the Lockout Policy (5 failed attempts), and managing user roles for every function call. This reinforced the necessity of the Principle of Least Privilege. I also ensured the Check-in/out flow was transactional, ensuring that the time logs were accurate and immediately updated, laying a reliable foundation for all security features that followed."


---

## 3. [Member 3 Name]'s Reflection: Security & Emerging Tech Specialist
"My focus was on the Information Assurance aspect, particularly the Detective Controls and system compliance. A core learning experience was designing the Audit Log (activity_log.py) as an immutable, central source of truth for all security events (FR-005). My most critical contribution was integrating the AI Anomaly Detector logic, which required me to think analytically about potential threat vectors and define clear, measurable parameters for anomalous behavior. I deliberately ensured the AI was advisory only to mitigate the R-003 risk of false positives. I gained valuable experience implementing practical security features, such as the 3-history password reuse check and the Admin's log filtering/export functionality, which transformed raw data into actionable security intelligence."



