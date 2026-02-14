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
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def valid_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    if not password.isalnum():
        return False, "Use only letters and numbers"
    return True, ""

def valid_answer(answer):
    if not answer or answer.strip() == "":
        return False, "Answer cannot be empty"
    if len(answer.strip()) < 2:
        return False, "Answer too short"
    if not re.match(r'^[a-zA-Z\s]+$', answer):
        return False, "Use only letters"
    return True, ""

def valid_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Use letters, numbers, _"
    return True, ""

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

# ================= COMPACT SIGNUP =================
def signup():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Sign Up</h1>', unsafe_allow_html=True)

    # Two columns for better space utilization
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Username", placeholder="Username", key="signup_username")
        password = st.text_input("Password", type="password", placeholder="Password", key="signup_password")
        security_question = st.selectbox("Security Question", [
            "Pet name?",
            "Mother's maiden name?",
            "Favorite teacher?"
        ], key="signup_question")
    
    with col2:
        email = st.text_input("Email", placeholder="Email", key="signup_email")
        confirm = st.text_input("Confirm", type="password", placeholder="Confirm", key="signup_confirm")
        security_answer = st.text_input("Answer", placeholder="Answer", key="signup_answer")

    if st.button("Register", key="signup_button"):
        # Quick validations
        if not all([username, email, password, confirm, security_answer]):
            st.error("All fields required")
            return

        # Validate
        is_valid_user, user_msg = valid_username(username)
        if not is_valid_user:
            st.error(user_msg)
            return

        if not valid_email(email):
            st.error("Invalid email")
            return

        is_valid_pass, pass_msg = valid_password(password)
        if not is_valid_pass:
            st.error(pass_msg)
            return

        if password != confirm:
            st.error("Passwords don't match")
            return

        is_valid_ans, ans_msg = valid_answer(security_answer)
        if not is_valid_ans:
            st.error(ans_msg)
            return

        if check_email_exists(email):
            st.error("Email exists")
            return

        try:
            cursor.execute(
                "INSERT INTO users (username,email,password,security_question,security_answer) VALUES (?,?,?,?,?)",
                (username, email, hash_password(password), security_question, hash_password(security_answer.strip()))
            )
            conn.commit()
            st.success("Account created!")
            # Clear form
            for key in ['signup_username', 'signup_email', 'signup_password', 'signup_confirm', 'signup_answer']:
                if key in st.session_state:
                    del st.session_state[key]
            import time
            time.sleep(1.5)
            st.session_state.page = "login"
            st.rerun()
        except Exception as e:
            st.error("Registration failed")

    # Compact link
    st.markdown('<p style="text-align: center; margin-top: 1rem;">', unsafe_allow_html=True)
    if st.button("← Back to Login", key="back_to_login"):
        st.session_state.page = "login"
        st.rerun()
    st.markdown('</p>', unsafe_allow_html=True)

    st.markdown(Templates.container_end(), unsafe_allow_html=True)

# ================= COMPACT LOGIN =================
def login():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Welcome Back</h1>', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Email", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Password", key="login_password")

    if st.button("Login", key="login_button"):
        if not email or not password:
            st.error("Enter email and password")
            return

        cursor.execute("SELECT username,password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()

        if user and user[1] == hash_password(password):
            token = create_token(email, user[0])
            st.session_state.token = token
            st.success("Welcome!")
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

    # Compact buttons in one row
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up", key="goto_signup"):
            st.session_state.page = "signup"
            st.rerun()
    with col2:
        if st.button("Forgot Password", key="goto_forgot"):
            st.session_state.page = "forgot"
            st.rerun()

    st.markdown(Templates.container_end(), unsafe_allow_html=True)

# ================= COMPACT DASHBOARD =================
def dashboard():
    payload = verify_token(st.session_state.token)
    if not payload:
        st.warning("Session expired")
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()
        return

    st.markdown(Templates.dashboard_container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: white; margin-bottom: 2rem;">Hello, {payload["username"]}!</h2>', unsafe_allow_html=True)

    if st.button("Logout", key="logout_button"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    st.markdown(Templates.dashboard_container_end(), unsafe_allow_html=True)

# ================= COMPACT FORGOT PASSWORD =================
def forgot_password():
    st.markdown(Templates.container_start(), unsafe_allow_html=True)
    st.markdown(Templates.logo(), unsafe_allow_html=True)

    st.markdown('<h1 class="page-title">Reset Password</h1>', unsafe_allow_html=True)

    if not st.session_state.reset_email:
        email = st.text_input("Email", placeholder="Your email", key="forgot_email")

        if st.button("Verify", key="verify_email"):
            if not email:
                st.error("Enter email")
                return

            cursor.execute("SELECT security_question FROM users WHERE email=?", (email,))
            user = cursor.fetchone()

            if user:
                st.session_state.reset_email = email
                st.session_state.security_question = user[0]
                st.rerun()
            else:
                st.error("Email not found")
    else:
        st.markdown(f'<p style="color: #4F8BF9; text-align: center; margin-bottom: 1rem;">{st.session_state.security_question}</p>', unsafe_allow_html=True)

        answer = st.text_input("Answer", placeholder="Your answer", key="security_answer")
        new_password = st.text_input("New Password", type="password", placeholder="New password", key="new_password")

        if st.button("Reset", key="reset_button"):
            if not answer or not new_password:
                st.error("All fields required")
                return

            is_valid_pass, pass_msg = valid_password(new_password)
            if not is_valid_pass:
                st.error(pass_msg)
                return

            cursor.execute("SELECT security_answer FROM users WHERE email=?", (st.session_state.reset_email,))
            stored_answer = cursor.fetchone()

            if stored_answer and stored_answer[0] == hash_password(answer.strip()):
                cursor.execute("UPDATE users SET password=? WHERE email=?",
                               (hash_password(new_password), st.session_state.reset_email))
                conn.commit()
                st.success("Password updated!")
                st.session_state.page = "login"
                st.session_state.reset_email = None
                st.session_state.security_question = None
                st.rerun()
            else:
                st.error("Wrong answer")

    # Back link
    if st.button("← Back", key="back_from_forgot"):
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
