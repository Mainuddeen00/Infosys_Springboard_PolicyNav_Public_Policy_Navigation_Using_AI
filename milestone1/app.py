%%writefile app.py
import streamlit as st
import sqlite3
import jwt
import datetime
import hashlib
import re
from styles import CSS
from templates import Templates

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="PolicyNav - Secure Access",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= APPLY CSS =================
st.markdown(CSS, unsafe_allow_html=True)

# ================= CONFIG =================
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    security_question TEXT NOT NULL,
    security_answer TEXT NOT NULL
)
""")
conn.commit()

# ================= UTILS =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(email, username):
    payload = {
        "sub": email,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

def valid_email(email):
    pattern = r'^[^@]+@[^@]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def check_email_exists(email):
    cursor.execute("SELECT email FROM users WHERE email=?", (email,))
    return cursor.fetchone() is not None

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "token" not in st.session_state:
    st.session_state.token = None
    
if "reset_email" not in st.session_state:
    st.session_state.reset_email = None
    
if "security_question" not in st.session_state:
    st.session_state.security_question = None

if "signup_success" not in st.session_state:
    st.session_state.signup_success = False

# ================= SIGNUP =================
def signup():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Create Account</h1>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
    email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
    confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")

    st.markdown(Templates.divider(), unsafe_allow_html=True)

    security_question = st.selectbox("Security Question", [
        "What is your pet name?",
        "What is your mother’s maiden name?",
        "What is your favorite teacher?"
    ], key="signup_question")

    security_answer = st.text_input("Security Answer", placeholder="Your answer", key="signup_answer")

    if st.button("Register", key="signup_button"):
        # Validate all fields
        if not all([username, email, password, confirm, security_answer]):
            st.error("❌ All fields are mandatory")
            return

        if not valid_email(email):
            st.error("❌ Invalid email format")
            return

        if password != confirm:
            st.error("❌ Passwords do not match")
            return

        # Check if email already exists
        if check_email_exists(email):
            st.error("❌ Email already exists")
            return

        try:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (username,email,password,security_question,security_answer) VALUES (?,?,?,?,?)",
                (username, email, hash_password(password), security_question, hash_password(security_answer))
            )
            conn.commit()
            st.success("✅ Account created successfully!")
            st.session_state.signup_success = True
            # Clear form by resetting the keys
            for key in ['signup_username', 'signup_email', 'signup_password', 'signup_confirm', 'signup_answer']:
                if key in st.session_state:
                    del st.session_state[key]
            # Redirect to login after 2 seconds
            import time
            time.sleep(2)
            st.session_state.page = "login"
            st.rerun()
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

    st.markdown(Templates.divider(), unsafe_allow_html=True)

    if st.button("← Back to Login", key="back_to_login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown(Templates.container_end(), unsafe_allow_html=True)

# ================= LOGIN =================
def login():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Welcome Back</h1>', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Enter your email", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

    if st.button("Login", key="login_button"):
        if not email or not password:
            st.error("❌ Please enter both email and password")
            return
            
        cursor.execute("SELECT username,password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user and user[1] == hash_password(password):
            token = create_token(email, user[0])
            st.session_state.token = token
            st.success("✅ Login successful!")
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("❌ Invalid email or password")

    st.markdown(Templates.divider(), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account", key="goto_signup"):
            st.session_state.page = "signup"
            st.rerun()
    
    with col2:
        if st.button("Forgot Password", key="goto_forgot"):
            st.session_state.page = "forgot"
            st.rerun()

    st.markdown(Templates.container_end(), unsafe_allow_html=True)

# ================= DASHBOARD =================
def dashboard():
    payload = verify_token(st.session_state.token)
    if not payload:
        st.warning("⚠️ Session expired")
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()
        return

    st.markdown(Templates.dashboard_container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown(Templates.welcome_message(payload['username']), unsafe_allow_html=True)

    if st.button("Logout", key="logout_button"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    st.markdown(Templates.dashboard_container_end(), unsafe_allow_html=True)

# ================= FORGOT PASSWORD =================
def forgot_password():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Reset Password</h1>', unsafe_allow_html=True)

    if not st.session_state.reset_email:
        email = st.text_input("Enter Email", placeholder="Your registered email", key="forgot_email")

        if st.button("Verify Email", key="verify_email"):
            if not email:
                st.error("❌ Please enter your email")
                return
                
            cursor.execute("SELECT security_question FROM users WHERE email=?", (email,))
            user = cursor.fetchone()

            if user:
                st.session_state.reset_email = email
                st.session_state.security_question = user[0]
                st.rerun()
            else:
                st.error("❌ Email not found")
    else:
        st.markdown(Templates.info_box(st.session_state.security_question), unsafe_allow_html=True)

        answer = st.text_input("Enter Security Answer", placeholder="Your answer", key="security_answer")
        new_password = st.text_input("New Password", type="password", placeholder="Enter new password", key="new_password")

        if st.button("Reset Password", key="reset_button"):
            if not answer or not new_password:
                st.error("❌ Please fill all fields")
                return
                
            cursor.execute("SELECT security_answer FROM users WHERE email=?", (st.session_state.reset_email,))
            stored_answer = cursor.fetchone()

            if stored_answer and stored_answer[0] == hash_password(answer):
                cursor.execute("UPDATE users SET password=? WHERE email=?",
                               (hash_password(new_password), st.session_state.reset_email))
                conn.commit()
                st.success("✅ Password updated successfully!")
                st.session_state.page = "login"
                st.session_state.reset_email = None
                st.session_state.security_question = None
                st.rerun()
            else:
                st.error("❌ Incorrect security answer")

    st.markdown(Templates.divider(), unsafe_allow_html=True)

    if st.button("← Back to Login", key="back_from_forgot"):
        st.session_state.page = "login"
        st.session_state.reset_email = None
        st.session_state.security_question = None
        st.rerun()

    st.markdown(Templates.container_end(), unsafe_allow_html=True)

# ================= ROUTING =================
if st.session_state.token:
    dashboard()
else:
    if st.session_state.page == "signup":
        signup()
    elif st.session_state.page == "forgot":
        forgot_password()
    else:
        login()
