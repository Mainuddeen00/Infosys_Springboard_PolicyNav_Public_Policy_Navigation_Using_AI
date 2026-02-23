# PolicyNav - Milestone 2

## 🔐 Enhanced Authentication System

### Features Implemented

#### 1. OTP-Based Authentication
- Secure email OTP for password reset
- 6-digit OTP valid for 10 minutes
- Resend OTP option available

#### 2. Account Lock Mechanism
- 3 failed login attempts = 5 minute lock
- Real-time countdown display
- Automatic unlock after timeout

#### 3. Password History
- Cannot reuse last 5 passwords
- Secure bcrypt hashing
- Password strength validation

#### 4. Readability Dashboard
- Analyze text readability
- Upload TXT/PDF files
- Visual gauges for metrics
- Grade level determination

#### 5. Enhanced UI/UX
- Permanent sidebar navigation
- Dark theme throughout
- Responsive design
- Professional styling

## 📸 Screenshots

### Login Page

<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 07 05 PM" src="https://github.com/user-attachments/assets/6583fdbd-fbbf-4f85-9683-9ba5c6eddbde" />

### Signup Page

<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 08 32 PM" src="https://github.com/user-attachments/assets/7e9bec99-7af8-4446-a9b5-ed5266edcafd" />

### Dashboard with Sidebar
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 07 22 PM" src="https://github.com/user-attachments/assets/40a2f1a1-3f23-4960-9ed4-b632410c0cc5" />
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 07 29 PM" src="https://github.com/user-attachments/assets/42ac319f-751d-4a9e-b461-744842323cff" />
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 07 43 PM" src="https://github.com/user-attachments/assets/a0a4e40d-e95d-4b21-8100-49260c559be1" />




### Readability Analyzer
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 07 50 PM" src="https://github.com/user-attachments/assets/94da907f-94a3-4f9e-a205-dea4403e8191" />



### OTP Email
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 08 08 PM" src="https://github.com/user-attachments/assets/68d820ae-9b2b-450d-9294-4fe071a6cee1" />


### Account Lock Feature
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 10 09 22 PM" src="https://github.com/user-attachments/assets/4ec9ab30-b0df-4103-a8aa-860d63551b90" />


## 🚀 How to Run

1. Open the Colab notebook
2. Add required secrets:
   - `EMAIL_ID` - Your Gmail
   - `EMAIL_APP_PASSWORD` - 16-digit app password
   - `NGROK_AUTHTOKEN` - Your ngrok token
3. Run all cells in order
4. Click the generated URL

## 📁 Files Included
- `app.py` - Main application
- `styles.py` - CSS styling
- `templates.py` - HTML templates
- `readability.py` - Readability analyzer
- Screenshots (png files)

## ✅ Testing Instructions
1. Register a new user
2. Login with credentials
3. Test Forgot Password with OTP
4. Try 3 wrong logins to trigger lock
5. Test Readability with sample text
6. Upload PDF/TXT files
