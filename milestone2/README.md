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
![Login Page](login_page.png)

### Signup Page
![Signup Page](signup_page.png)

### Dashboard with Sidebar
![Dashboard](dashboard.png)

### Readability Analyzer
![Readability Analyzer](readability.png)

### OTP Email
![OTP Email](otp_email.png)

### Account Lock Feature
![Account Lock](account_lock.png)

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
