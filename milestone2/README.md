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

### Dashboard with Sidebar
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 7 39 51 PM" src="https://github.com/user-attachments/assets/d397c5a8-9fa7-4964-b66f-cc77813cdbcf" />


### Readability Analyzer
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 7 40 01 PM" src="https://github.com/user-attachments/assets/4899b7a7-843a-427f-aa53-41fcf805af33" />
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 7 40 07 PM" src="https://github.com/user-attachments/assets/a5ed813f-1e4a-4a87-9481-509de378ac4a" />
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 7 40 24 PM" src="https://github.com/user-attachments/assets/f7cd448a-f3f0-464e-a686-1062e67ae201" />


### OTP Email
<img width="1440" height="900" alt="Screenshot 2026-02-23 at 7 39 30 PM" src="https://github.com/user-attachments/assets/f16b4895-3dc0-4708-a675-40d7ebb66734" />

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
