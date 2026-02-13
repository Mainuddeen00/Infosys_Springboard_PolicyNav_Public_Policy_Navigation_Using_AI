# Milestone 1 – Secure User Authentication System

## 📌 Project Title
PolicyNav – Public Policy Navigation Using AI  
Milestone 1: Secure User Authentication Module

---

## 🧾 Description

In this milestone, a secure user authentication system was developed using **Streamlit**, **JWT (JSON Web Token)**, **SQLite**, and **Ngrok**.

This authentication module serves as the foundation for the PolicyNav project and ensures secure user registration, login, session management, and password recovery.

---

## 🚀 Technologies Used

- Python 3
- Streamlit (Frontend UI)
- SQLite (Database)
- JWT – JSON Web Token (Authentication & Session Management)
- hashlib (Password Hashing using SHA-256)
- Ngrok (Expose local app to public URL)

---

## 🔐 Features Implemented

### ✅ 1. User Signup
- Username (Mandatory)
- Email (Validated format)
- Password (Alphanumeric validation)
- Confirm Password (Must match)
- Security Question (Dropdown)
- Security Answer
- Password stored securely using hashing
- Data stored in SQLite database

---

### ✅ 2. Secure Login
- Email verification from database
- Password hash comparison
- JWT token generation upon successful login
- Token expiration (30 minutes session time)

---

### ✅ 3. Dashboard
- Welcome message displaying username
- JWT verification before access
- Logout functionality

---

### ✅ 4. Forgot Password Flow
1. User enters registered email
2. System verifies email existence
3. Displays stored security question
4. User enters correct security answer
5. Allows password reset
6. Updates password securely in database

---

### ✅ 5. JWT Authentication
- Token generated after login
- Token contains:
  - User email
  - Username
  - Expiration time
- Token verified on every dashboard access
- Expired or tampered tokens are rejected

---

### ✅ 6. Ngrok Integration
- Application exposed to internet using Ngrok
- Link: https://ngrok.com/
- Public URL generated for demonstration
- Ngrok authtoken removed before GitHub upload (for security)

---

## 🗄 Database Structure

SQLite database file: `users.db`

Table: `users`

| Column              | Type    |
|---------------------|---------|
| id                  | INTEGER |
| username            | TEXT    |
| email               | TEXT (Unique) |
| password            | TEXT (Hashed) |
| security_question   | TEXT    |
| security_answer     | TEXT (Hashed) |

---

## ▶ How to Run the Application (Local Setup)

### Step 1: Install Dependencies

```bash
pip install streamlit pyjwt
streamlit run app.py
ngrok http 8501
```

<img width="1440" height="900" alt="Screenshot 2026-02-13 at 8 18 32 PM" src="https://github.com/user-attachments/assets/0eee6530-99ea-41e5-88e7-13ac1e667f64" />


<img width="1440" height="900" alt="Screenshot 2026-02-13 at 8 18 45 PM" src="https://github.com/user-attachments/assets/17d8d785-0acf-4fac-82a5-5c1904e20251" />


<img width="1440" height="900" alt="Screenshot 2026-02-13 at 8 18 52 PM" src="https://github.com/user-attachments/assets/2a3321f8-0f81-4e9c-bba5-4126928ad1b0" />



