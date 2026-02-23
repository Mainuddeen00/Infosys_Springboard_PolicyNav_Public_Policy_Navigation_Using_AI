%%writefile app.py
import streamlit as st
import sqlite3
import jwt
import datetime
import hashlib
import re
import time
import bcrypt
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from styles import CSS
from templates import Templates
import readability
import PyPDF2

# ================= LOAD SECRETS FROM ENVIRONMENT =================
EMAIL_ADDRESS = os.environ.get('EMAIL_ID')
EMAIL_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD')
SECRET_KEY = os.environ.get('JWT_SECRET', 'fallback-secret-key-change-me')

# ================= ADMIN CREDENTIALS =================
ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL', 'admin@policynav.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="PolicyNav - Secure Access",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= APPLY CSS =================
st.markdown(CSS, unsafe_allow_html=True)

# ================= CONFIG =================
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_TIME = 300
OTP_EXPIRY_MINUTES = 10

# ================= DATABASE =================
conn   = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    security_question TEXT NOT NULL,
    security_answer TEXT NOT NULL,
    created_at TEXT,
    is_blocked INTEGER DEFAULT 0
)""")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN is_blocked INTEGER DEFAULT 0")
    conn.commit()
except:
    pass

cursor.execute("""
CREATE TABLE IF NOT EXISTS password_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    set_at TEXT,
    FOREIGN KEY(email) REFERENCES users(email)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS login_attempts (
    email TEXT PRIMARY KEY,
    attempts INTEGER DEFAULT 0,
    last_attempt REAL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS otp_requests (
    email TEXT PRIMARY KEY,
    otp TEXT,
    expires_at REAL
)""")

conn.commit()

# ================= UTILITY FUNCTIONS =================
def _get_timestamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(email, username, role="user"):
    payload = {
        "sub": email,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

# ================= VALIDATION FUNCTIONS =================
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

# ================= RATE LIMITING FUNCTIONS =================
def get_login_attempts(email):
    cursor.execute("SELECT attempts, last_attempt FROM login_attempts WHERE email = ?", (email,))
    data = cursor.fetchone()
    return data if data else (0, 0)

def increment_login_attempts(email):
    attempts, _ = get_login_attempts(email)
    cursor.execute("INSERT OR REPLACE INTO login_attempts (email, attempts, last_attempt) VALUES (?, ?, ?)",
                   (email, attempts + 1, time.time()))
    conn.commit()

def reset_login_attempts(email):
    cursor.execute("DELETE FROM login_attempts WHERE email = ?", (email,))
    conn.commit()

def is_rate_limited(email):
    attempts, last_attempt = get_login_attempts(email)
    if attempts >= MAX_LOGIN_ATTEMPTS:
        if time.time() - last_attempt < LOCKOUT_TIME:
            return True, LOCKOUT_TIME - (time.time() - last_attempt)
        else:
            reset_login_attempts(email)
    return False, 0

# ================= USER MANAGEMENT FUNCTIONS =================
def register_user(username, email, password, security_question, security_answer):
    try:
        now = _get_timestamp()
        hashed_pass   = hash_password(password)
        hashed_answer = hash_password(security_answer.strip())
        cursor.execute(
            "INSERT INTO users (username, email, password, security_question, security_answer, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (username, email, hashed_pass, security_question, hashed_answer, now)
        )
        cursor.execute("INSERT INTO password_history (email, password, set_at) VALUES (?, ?, ?)",
                       (email, hashed_pass, now))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email, password):
    is_limited, _ = is_rate_limited(email)
    if is_limited:
        return False, "locked"
    cursor.execute("SELECT username, password, is_blocked FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        if user[2] == 1:
            return False, "blocked"
        if user[1] == hash_password(password):
            reset_login_attempts(email)
            return True, user[0]
    increment_login_attempts(email)
    return False, None

def authenticate_admin(email, password):
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD

def check_user_exists(email):
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    return cursor.fetchone() is not None

def get_user_details(email):
    cursor.execute("SELECT username, security_question, security_answer FROM users WHERE email = ?", (email,))
    return cursor.fetchone()

def check_password_reused(email, new_password):
    cursor.execute("SELECT password FROM password_history WHERE email = ? ORDER BY id DESC LIMIT 5", (email,))
    history = cursor.fetchall()
    hashed_new = hash_password(new_password)
    for (stored_hash,) in history:
        if stored_hash == hashed_new:
            return True
    return False

def update_password(email, new_password):
    hashed = hash_password(new_password)
    now    = _get_timestamp()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    cursor.execute("INSERT INTO password_history (email, password, set_at) VALUES (?, ?, ?)",
                   (email, hashed, now))
    conn.commit()
    reset_login_attempts(email)

def verify_security_answer(email, answer):
    cursor.execute("SELECT security_answer FROM users WHERE email = ?", (email,))
    stored_answer = cursor.fetchone()
    return stored_answer and stored_answer[0] == hash_password(answer.strip())

# ================= ADMIN USER MANAGEMENT =================
def get_all_users():
    cursor.execute("SELECT id, username, email, created_at, is_blocked FROM users ORDER BY id DESC")
    return cursor.fetchall()

def block_user(email):
    cursor.execute("UPDATE users SET is_blocked = 1 WHERE email = ?", (email,))
    conn.commit()

def unblock_user(email):
    cursor.execute("UPDATE users SET is_blocked = 0 WHERE email = ?", (email,))
    conn.commit()

def delete_user(email):
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    cursor.execute("DELETE FROM password_history WHERE email = ?", (email,))
    cursor.execute("DELETE FROM login_attempts WHERE email = ?", (email,))
    cursor.execute("DELETE FROM otp_requests WHERE email = ?", (email,))
    conn.commit()

def get_user_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_blocked = 1")
    blocked = cursor.fetchone()[0]
    return total, blocked, total - blocked

# ================= OTP FUNCTIONS =================
def generate_otp():
    return f"{secrets.randbelow(1000000):06d}"

def save_otp(email, otp):
    expires_at = time.time() + (OTP_EXPIRY_MINUTES * 60)
    cursor.execute("INSERT OR REPLACE INTO otp_requests (email, otp, expires_at) VALUES (?, ?, ?)",
                   (email, otp, expires_at))
    conn.commit()

def verify_otp(email, otp):
    cursor.execute("SELECT otp, expires_at FROM otp_requests WHERE email = ?", (email,))
    data = cursor.fetchone()
    if data and data[0] == otp and time.time() < data[1]:
        cursor.execute("DELETE FROM otp_requests WHERE email = ?", (email,))
        conn.commit()
        return True
    return False

def send_otp_email(to_email, otp):
    try:
        msg            = MIMEMultipart()
        msg['From']    = f"PolicyNav <{EMAIL_ADDRESS}>"
        msg['To']      = to_email
        msg['Subject'] = "🔐 PolicyNav - Password Reset OTP"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0E1117; color: #ffffff; padding: 20px;">
            <div style="max-width: 400px; margin: 0 auto; background: #1e2530; border: 1px solid #2e3642; border-radius: 10px; padding: 30px;">
                <h2 style="color: #4F8BF9; text-align: center;">PolicyNav</h2>
                <p style="text-align: center;">Your OTP for password reset is:</p>
                <h1 style="color: #4F8BF9; text-align: center; font-size: 36px; letter-spacing: 5px;">{otp}</h1>
                <p style="text-align: center; color: #8b9bb4;">Valid for {OTP_EXPIRY_MINUTES} minutes</p>
            </div>
        </body>
        </html>"""
        msg.attach(MIMEText(body, 'html'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True, "OTP sent successfully!"
    except Exception as e:
        return False, str(e)

# ================= TOOLTIP HELPER =================
def tooltip(icon_label, title, description):
    return f"""
    <div class="metric-title">
        {icon_label}
        <div class="tooltip-wrap">
            <span class="tooltip-icon">?</span>
            <div class="tooltip-box">
                <strong>{title}</strong>
                <p>{description}</p>
            </div>
        </div>
    </div>"""

def metric_card(label, tooltip_title, tooltip_desc, value, bar_pct, bar_color, interpretation, icon):
    bar_pct_clamped = max(0, min(100, bar_pct))
    return f"""
    <div class="metric-card">
        {tooltip(icon + " " + label, tooltip_title, tooltip_desc)}
        <div class="metric-value">{value:.1f}</div>
        <div class="metric-bar-track">
            <div class="metric-bar-fill" style="width:{bar_pct_clamped}%; background:{bar_color};"></div>
        </div>
        <p class="metric-interpretation">{interpretation}</p>
    </div>"""

# ================= SESSION =================
_session_defaults = {
    "page": "login", "token": None, "role": "user",
    "reset_email": None, "security_question": None,
    "otp_verified": False, "username": None,
    "menu_option": "Dashboard", "reset_method": None, "otp_sent": False,
}
for _k, _v in _session_defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ================= PROFESSIONAL USER DASHBOARD =================
def dashboard_page(username):
    now_dt = datetime.datetime.now()
    hour   = now_dt.hour
    if hour < 12:
        greeting = "Good morning"
        greet_icon = "🌤️"
    elif hour < 17:
        greeting = "Good afternoon"
        greet_icon = "☀️"
    else:
        greeting = "Good evening"
        greet_icon = "🌙"

    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        st.markdown(f"""
        <div style="margin-bottom: 2rem; margin-top: 4rem; text-align: center;">
            <p style="color: #4a5a72; font-size: 0.85rem; margin: 0 0 0.2rem 0; text-transform: uppercase; letter-spacing: 0.06em;">{greet_icon} {greeting}</p>
            <h1 class="page-title" style="margin-bottom: 0.2rem; font-size: 2.5rem;">{username}</h1>
            <p style="color: #4a5a72; font-size: 0.9rem; margin: 0;">{now_dt.strftime("%A, %B %d, %Y")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem;">
            <p style="color: #8e8ea0; font-size: 1.1rem;">Select a tool from the sidebar to get started.</p>
        </div>
        """, unsafe_allow_html=True)


# ================= PROFESSIONAL READABILITY PAGE =================
def readability_page():
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 class="page-title" style="margin-bottom: 0.2rem;">Readability Analyzer</h1>
        <p style="color: #4a5a72; font-size: 0.88rem; margin: 0;">
            Measure how easy your text is to read using industry-standard formulas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✍️  Paste Text", "📂  Upload File"])
    text_input = ""

    with tab1:
        raw_text = st.text_area(
            "Enter your text below",
            height=180,
            placeholder="Paste any text here — policy documents, articles, essays...",
            key="readability_text"
        )
        if raw_text:
            text_input = raw_text
        st.markdown(f"<p style='color:#2a3547; font-size:0.75rem; margin-top:0.3rem;'>{len(raw_text.split()) if raw_text else 0} words · {len(raw_text) if raw_text else 0} characters</p>", unsafe_allow_html=True)

    with tab2:
        uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"], key="readability_file")
        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(uploaded_file)
                    text   = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    text_input = text
                    st.success(f"✅ Loaded {len(reader.pages)} page(s) from PDF")
                else:
                    text_input = uploaded_file.read().decode("utf-8")
                    st.success(f"✅ Loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {e}")

    analyze_clicked = st.button("Analyze Text", type="primary", key="analyze_button")

    if analyze_clicked:
        if len(text_input.strip()) < 50:
            st.error("Text is too short. Please enter at least 50 characters.")
        else:
            with st.spinner("Analyzing readability..."):
                analyzer = readability.ReadabilityAnalyzer(text_input)
                scores   = analyzer.get_all_metrics()

            flesch_ease  = scores["Flesch Reading Ease"]
            fk_grade     = scores["Flesch-Kincaid Grade"]
            smog         = scores["SMOG Index"]
            gunning      = scores["Gunning Fog"]
            coleman      = scores["Coleman-Liau"]

            avg_grade = (fk_grade + gunning + smog + coleman) / 4

            if avg_grade <= 6:
                level      = "Beginner"
                sublevel   = "Elementary School"
                level_icon = "🟢"
                lv_color   = "#10b981"
                lv_bg      = "rgba(16,185,129,0.1)"
                lv_desc    = "Very easy to read. Suitable for general public communication."
            elif avg_grade <= 10:
                level      = "Intermediate"
                sublevel   = "Middle School"
                level_icon = "🔵"
                lv_color   = "#4F8BF9"
                lv_bg      = "rgba(79,139,249,0.1)"
                lv_desc    = "Easy to read. Clear language for a broad audience."
            elif avg_grade <= 14:
                level      = "Advanced"
                sublevel   = "High School / College"
                level_icon = "🟡"
                lv_color   = "#f59e0b"
                lv_bg      = "rgba(245,158,11,0.1)"
                lv_desc    = "Moderately complex. Requires good reading skills."
            else:
                level      = "Expert"
                sublevel   = "Professional / Academic"
                level_icon = "🔴"
                lv_color   = "#ef4444"
                lv_bg      = "rgba(239,68,68,0.1)"
                lv_desc    = "Very complex. Best suited for technical or academic readers."

            st.markdown(f"""
            <div class="level-banner" style="border-color: {lv_color}33;">
                <div class="level-icon" style="background: {lv_bg}; font-size:1.8rem;">{level_icon}</div>
                <div>
                    <p class="level-title">{level} Level</p>
                    <p class="level-desc">{sublevel} · {lv_desc}</p>
                </div>
                <div class="level-grade">
                    <p class="level-grade-num" style="color:{lv_color};">{avg_grade:.1f}</p>
                    <p class="level-grade-label">Grade Level</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="section-header" style="margin-top:0.5rem;">
                <h2>Readability Scores</h2>
                <span>Hover the <b>?</b> icon on each metric to learn what it means</span>
            </div>""", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            flesch_interp = (
                "Very Easy" if flesch_ease >= 90 else
                "Easy" if flesch_ease >= 70 else
                "Fairly Easy" if flesch_ease >= 60 else
                "Standard" if flesch_ease >= 50 else
                "Fairly Difficult" if flesch_ease >= 30 else
                "Difficult"
            )
            with col1:
                st.markdown(metric_card(
                    "Flesch Reading Ease",
                    "Flesch Reading Ease",
                    "Scores text from 0–100. Higher = easier to read. A score of 60–70 is ideal for general audiences. Very low scores mean the text is academic or legal in nature.",
                    flesch_ease,
                    flesch_ease,
                    "#4F8BF9",
                    f"Interpretation: {flesch_interp}",
                    "📘"
                ), unsafe_allow_html=True)

            with col2:
                fk_interp = f"~Grade {fk_grade:.0f} reading level"
                st.markdown(metric_card(
                    "Flesch-Kincaid Grade",
                    "Flesch-Kincaid Grade Level",
                    "Converts readability to a US school grade number. Grade 8 = readable by most adults. Grade 12+ = college-level. The higher the number, the harder the text.",
                    fk_grade,
                    (fk_grade / 20) * 100,
                    "#7c3aed",
                    fk_interp,
                    "🎓"
                ), unsafe_allow_html=True)

            with col3:
                smog_interp = f"Requires approximately {smog:.0f} years of education"
                st.markdown(metric_card(
                    "SMOG Index",
                    "SMOG Index (Simple Measure of Gobbledygook)",
                    "Estimates how many years of education someone needs to understand your text. Focuses on counting complex words (3+ syllables). A score of 8 is ideal for public-facing content.",
                    smog,
                    (smog / 20) * 100,
                    "#10b981",
                    smog_interp,
                    "🔬"
                ), unsafe_allow_html=True)

            col4, col5 = st.columns(2)

            with col4:
                fog_interp = (
                    "Accessible — easy for most readers" if gunning < 8 else
                    "Standard — comfortable reading level" if gunning < 12 else
                    "Academic — requires focused reading" if gunning < 16 else
                    "Very dense — specialist audience"
                )
                st.markdown(metric_card(
                    "Gunning Fog Index",
                    "Gunning Fog Index",
                    "Measures how many years of formal education a reader needs. It looks at sentence length and the percentage of complex words. Below 12 is ideal for wide readership.",
                    gunning,
                    (gunning / 20) * 100,
                    "#f59e0b",
                    fog_interp,
                    "🌫️"
                ), unsafe_allow_html=True)

            with col5:
                cl_interp = f"~Grade {coleman:.0f} level — based on characters per word"
                st.markdown(metric_card(
                    "Coleman-Liau Index",
                    "Coleman-Liau Index",
                    "Unlike other formulas, this uses characters (not syllables) to estimate grade level. It counts average letters per 100 words and sentences per 100 words. More accurate for digital text.",
                    coleman,
                    (coleman / 20) * 100,
                    "#ef4444",
                    cl_interp,
                    "🔢"
                ), unsafe_allow_html=True)

            st.markdown("""
            <div class="section-header" style="margin-top:1.5rem;">
                <h2>Text Statistics</h2>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="stat-row">
                <div class="stat-pill">
                    <span class="stat-pill-value">{analyzer.num_sentences}</span>
                    <span class="stat-pill-label">Sentences</span>
                </div>
                <div class="stat-pill">
                    <span class="stat-pill-value">{analyzer.num_words}</span>
                    <span class="stat-pill-label">Words</span>
                </div>
                <div class="stat-pill">
                    <span class="stat-pill-value">{analyzer.num_syllables}</span>
                    <span class="stat-pill-label">Syllables</span>
                </div>
                <div class="stat-pill">
                    <span class="stat-pill-value">{analyzer.complex_words}</span>
                    <span class="stat-pill-label">Complex Words</span>
                </div>
                <div class="stat-pill">
                    <span class="stat-pill-value">{analyzer.char_count}</span>
                    <span class="stat-pill-label">Characters</span>
                </div>
                <div class="stat-pill">
                    <span class="stat-pill-value">{round(analyzer.num_words / max(analyzer.num_sentences, 1), 1)}</span>
                    <span class="stat-pill-label">Avg Words/Sent</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ================= ADMIN DASHBOARD PAGE =================
def admin_dashboard_page():
    total, blocked, active = get_user_stats()

    st.markdown("""
    <div class="admin-section">
        <h2 style="color: #f59e0b; margin: 0; font-size:1.4rem; font-weight:700; letter-spacing:-0.02em;">🛡️ Admin Control Panel</h2>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><p class="stat-number">{total}</p><p class="stat-label">Total Users</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><p class="stat-number" style="color:#10b981">{active}</p><p class="stat-label">Active Users</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><p class="stat-number" style="color:#ef4444">{blocked}</p><p class="stat-label">Blocked Users</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-card"><p class="stat-number" style="color:#f59e0b;">∞</p><p class="stat-label">Admin Access</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    search_query = st.text_input("🔍 Search users by name or email", placeholder="Search...", key="admin_search")

    users = get_all_users()
    if search_query:
        users = [u for u in users if search_query.lower() in u[1].lower() or search_query.lower() in u[2].lower()]

    st.markdown(f"<p style='color:#4a5a72; font-size:0.8rem; margin-bottom:0.5rem;'>Showing {len(users)} user(s)</p>", unsafe_allow_html=True)

    if not users:
        st.markdown('<div style="text-align:center;padding:3rem;color:#4a5a72;"><h3>No users found</h3></div>', unsafe_allow_html=True)
        return

    st.markdown("""
    <div style="display:flex; padding:10px 16px; background:#080b12; border-radius:8px 8px 0 0; border:1px solid #1e2736; gap:1rem; margin-top:0.5rem;">
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:0.3;">#</span>
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:1;">Username</span>
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:1.5;">Email</span>
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:1;">Joined</span>
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:0.7;">Status</span>
        <span style="color:#4a5a72; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; flex:1.2;">Actions</span>
    </div>""", unsafe_allow_html=True)

    for user in users:
        uid, uname, uemail, ucreated, ublocked = user
        status_html = '<span class="status-blocked">Blocked</span>' if ublocked else '<span class="status-active">Active</span>'
        joined      = ucreated[:10] if ucreated else "N/A"

        st.markdown(f"""
        <div style="display:flex; align-items:center; padding:12px 16px; background:#0d1117;
             border:1px solid #1e2736; border-top:none; gap:1rem;">
            <span style="color:#4a5a72; flex:0.3; font-size:0.82rem; font-family:'DM Mono',monospace;">{uid}</span>
            <span style="color:#e2e8f0; flex:1; font-weight:500; font-size:0.88rem;">{uname}</span>
            <span style="color:#4a5a72; flex:1.5; font-size:0.82rem;">{uemail}</span>
            <span style="color:#4a5a72; flex:1; font-size:0.82rem; font-family:'DM Mono',monospace;">{joined}</span>
            <span style="flex:0.7;">{status_html}</span>
            <span style="flex:1.2;"></span>
        </div>""", unsafe_allow_html=True)

        col_block, col_delete, col_spacer = st.columns([1, 1, 3])
        with col_block:
            if ublocked:
                if st.button(f"✅ Unblock", key=f"unblock_{uid}", use_container_width=True):
                    unblock_user(uemail); st.success(f"Unblocked {uname}"); time.sleep(0.8); st.rerun()
            else:
                if st.button(f"🚫 Block", key=f"block_{uid}", use_container_width=True):
                    block_user(uemail); st.warning(f"Blocked {uname}"); time.sleep(0.8); st.rerun()
        with col_delete:
            if st.button(f"🗑️ Delete", key=f"delete_{uid}", use_container_width=True):
                if "confirm_delete" not in st.session_state:
                    st.session_state["confirm_delete"] = uemail
                    st.rerun()

        if st.session_state.get("confirm_delete") == uemail:
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.08); border:1px solid #ef444433; border-radius:8px;
                 padding:12px 16px; margin:4px 0 8px 0; color:#fca5a5; font-size:0.85rem;">
                ⚠️ Delete <strong>{uname}</strong>? This cannot be undone.
            </div>""", unsafe_allow_html=True)
            yes_col, no_col, _ = st.columns([1, 1, 4])
            with yes_col:
                if st.button("Yes, Delete", key=f"yes_del_{uid}", type="primary"):
                    delete_user(uemail); st.session_state.pop("confirm_delete", None)
                    st.success(f"Deleted {uname}"); time.sleep(0.8); st.rerun()
            with no_col:
                if st.button("Cancel", key=f"no_del_{uid}"):
                    st.session_state.pop("confirm_delete", None); st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ================= PAGE FUNCTIONS =================
def signup():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown('<h1 class="page-title" style="text-align: center;">Create Account</h1>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        col1, col2 = st.columns(2)
        with col1:
            username          = st.text_input("Username", placeholder="your_username", key="signup_username")
            password          = st.text_input("Password", type="password", placeholder="••••••••", key="signup_password")
            security_question = st.selectbox("Security Question", [
                "What is your pet name?",
                "What is your mother's maiden name?",
                "What is your favorite teacher?"
            ], key="signup_question")
        with col2:
            email           = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            confirm         = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")
            security_answer = st.text_input("Security Answer", placeholder="Your answer", key="signup_answer")

        if st.button("Create Account", key="signup_button", use_container_width=True, type="primary"):
            if not all([username, email, password, confirm, security_answer]):
                st.error("All fields required"); return
            is_valid_user, user_msg = valid_username(username)
            if not is_valid_user: st.error(user_msg); return
            if not valid_email(email): st.error("Invalid email format"); return
            is_valid_pass, pass_msg = valid_password(password)
            if not is_valid_pass: st.error(pass_msg); return
            if password != confirm: st.error("Passwords don't match"); return
            is_valid_ans, ans_msg = valid_answer(security_answer)
            if not is_valid_ans: st.error(ans_msg); return
            if check_user_exists(email): st.error("Email already exists"); return
            if register_user(username, email, password, security_question, security_answer):
                st.success("Account created successfully!")
                for key in ['signup_username','signup_email','signup_password','signup_confirm','signup_answer']:
                    if key in st.session_state: del st.session_state[key]
                time.sleep(1.5)
                st.session_state.page = "login"; st.rerun()
            else:
                st.error("Registration failed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Login", key="back_to_login", use_container_width=True):
            st.session_state.page = "login"; st.rerun()

def login():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown('<h1 class="page-title" style="text-align: center;">Welcome back</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle" style="text-align: center;">Sign in to your account</p>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        email    = st.text_input("Email", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

        is_limited, wait_time = is_rate_limited(email) if email else (False, 0)
        if is_limited:
            minutes = int(wait_time // 60)
            seconds = int(wait_time % 60)
            st.error(f"Account locked. Try again in {minutes}m {seconds}s")
        else:
            if st.button("Sign In", key="login_button", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("Enter email and password"); return
                auth_result, username = authenticate_user(email, password)
                if auth_result:
                    token = create_token(email, username, "user")
                    st.session_state.token       = token
                    st.session_state.username    = username
                    st.session_state.role        = "user"
                    st.session_state.page        = "dashboard"
                    st.session_state.menu_option = "Dashboard"
                    st.success("Login successful!")
                    time.sleep(1); st.rerun()
                elif username == "locked":
                    st.error("Account is locked. Please try again later.")
                elif username == "blocked":
                    st.error("Your account has been blocked. Please contact admin.")
                else:
                    attempts, _ = get_login_attempts(email)
                    attempts_left = MAX_LOGIN_ATTEMPTS - attempts
                    st.error(f"Invalid credentials. {attempts_left} attempts left")

        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Create Account", key="goto_signup", use_container_width=True):
                st.session_state.page = "signup"; st.rerun()
        with c2:
            if st.button("Forgot Password", key="goto_forgot", use_container_width=True):
                st.session_state.page = "forgot"; st.rerun()
        with c3:
            if st.button("🛡️ Admin", key="goto_admin_login", use_container_width=True):
                st.session_state.page = "admin_login"; st.rerun()

def admin_login():
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon" style="border-color: #f59e0b; box-shadow: 0 0 20px rgba(245,158,11,0.2);">
            <svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" style="width:2rem;height:2rem;">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <path d="M9 12l2 2 4-4"/>
            </svg>
        </div>
        <div class="logo-text">PolicyNav</div>
        <div class="logo-subtext" style="color: #f59e0b;">Admin Portal</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<h1 class="page-title" style="color:#f59e0b; text-align:center;">Admin Access</h1>', unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.2);
             border-radius:8px; padding:10px 14px; margin-bottom:1rem; text-align:center;">
            <span style="color:#f59e0b; font-size:0.82rem; letter-spacing:0.03em;">🔒 Restricted — Authorised Personnel Only</span>
        </div>""", unsafe_allow_html=True)

        admin_email = st.text_input("Admin Email",    placeholder="admin@policynav.com", key="admin_email")
        admin_pass  = st.text_input("Admin Password", type="password", placeholder="••••••••",    key="admin_pass")

        if st.button("Access Admin Panel", key="admin_login_btn", use_container_width=True, type="primary"):
            if not admin_email or not admin_pass:
                st.error("Enter credentials")
            elif authenticate_admin(admin_email, admin_pass):
                token = create_token(admin_email, "Admin", "admin")
                st.session_state.token       = token
                st.session_state.username    = "Admin"
                st.session_state.role        = "admin"
                st.session_state.page        = "dashboard"
                st.session_state.menu_option = "Dashboard"
                st.success("Welcome, Admin!")
                time.sleep(1); st.rerun()
            else:
                st.error("Invalid admin credentials")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to User Login", key="back_from_admin", use_container_width=True):
            st.session_state.page = "login"; st.rerun()

def forgot_password():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown('<h1 class="page-title" style="text-align: center;">Reset Password</h1>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        if not st.session_state.reset_email:
            email = st.text_input("Email", placeholder="Your registered email", key="forgot_email")
            st.markdown("""
            <p style="color:#4a5a72; text-align:center; margin:1rem 0 0.5rem; font-size:0.85rem; letter-spacing:0.02em;">
                Choose your verification method
            </p>""", unsafe_allow_html=True)
            col_otp, col_sec = st.columns(2)
            with col_otp:
                otp_btn = st.button("📧 Via OTP Email",    key="method_otp", use_container_width=True)
            with col_sec:
                sec_btn = st.button("🔑 Via Security Q&A", key="method_sec", use_container_width=True)

            if otp_btn or sec_btn:
                if not email:
                    st.error("Please enter your email first")
                elif not check_user_exists(email):
                    st.error("Email not found in our system")
                elif otp_btn:
                    otp     = generate_otp()
                    save_otp(email, otp)
                    success, msg = send_otp_email(email, otp)
                    if success:
                        st.session_state.reset_email  = email
                        st.session_state.reset_method = "otp"
                        st.success("OTP sent to your email!")
                        time.sleep(1); st.rerun()
                    else:
                        st.error(f"Failed to send OTP: {msg}")
                else:
                    st.session_state.reset_email  = email
                    st.session_state.reset_method = "security"
                    st.rerun()

        elif st.session_state.reset_method == "otp" and not st.session_state.otp_verified:
            st.markdown(f"""
            <div style="background:rgba(79,139,249,0.08); border:1px solid #4F8BF933; border-radius:8px;
                 padding:10px 14px; margin-bottom:1rem; text-align:center;">
                <span style="color:#4F8BF9; font-size:0.88rem;">
                    📧 OTP sent to <strong>{st.session_state.reset_email}</strong>
                </span>
            </div>""", unsafe_allow_html=True)
            otp_input = st.text_input("Enter OTP", placeholder="6-digit code", key="otp_input", max_chars=6)
            if st.button("Verify OTP", key="verify_otp", type="primary", use_container_width=True):
                if verify_otp(st.session_state.reset_email, otp_input):
                    st.session_state.otp_verified = True
                    st.success("OTP verified!"); st.rerun()
                else:
                    st.error("Invalid or expired OTP")
            if st.button("Resend OTP", key="resend_otp", use_container_width=True):
                otp = generate_otp(); save_otp(st.session_state.reset_email, otp)
                send_otp_email(st.session_state.reset_email, otp); st.success("New OTP sent!")

        elif st.session_state.reset_method == "security" and not st.session_state.otp_verified:
            user_details = get_user_details(st.session_state.reset_email)
            if user_details:
                _, security_question, _ = user_details
                st.markdown(f"""
                <div style="background:rgba(79,139,249,0.08); border:1px solid #4F8BF933; border-radius:8px;
                     padding:14px; margin-bottom:1rem; text-align:center;">
                    <p style="color:#4a5a72; margin:0 0 4px; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.06em;">Security Question</p>
                    <p style="color:#4F8BF9; margin:0; font-weight:600; font-size:0.9rem;">❓ {security_question}</p>
                </div>""", unsafe_allow_html=True)
                answer = st.text_input("Your Answer", placeholder="Enter your answer", key="sec_answer")
                if st.button("Verify Answer", key="verify_sec", type="primary", use_container_width=True):
                    if not answer:
                        st.error("Please enter your answer")
                    elif verify_security_answer(st.session_state.reset_email, answer):
                        st.session_state.otp_verified = True
                        st.success("Answer verified!"); time.sleep(0.8); st.rerun()
                    else:
                        st.error("Incorrect security answer")

        elif st.session_state.otp_verified:
            _new_password_form()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back", key="back_from_forgot", use_container_width=True):
            st.session_state.page         = "login"
            st.session_state.reset_email  = None
            st.session_state.otp_verified = False
            st.session_state.reset_method = None
            st.session_state.otp_sent     = False
            st.rerun()

def _new_password_form():
    st.markdown("""
    <div style="background:rgba(16,185,129,0.08); border:1px solid #10b98133; border-radius:8px;
         padding:10px 14px; margin-bottom:1rem; text-align:center;">
        <span style="color:#10b981; font-size:0.88rem;">✅ Identity verified — set your new password</span>
    </div>""", unsafe_allow_html=True)

    new_password     = st.text_input("New Password",     type="password", placeholder="••••••••", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="confirm_new_password")

    if st.button("Reset Password", key="reset_button", type="primary", use_container_width=True):
        if not new_password or not confirm_password:
            st.error("All fields required"); return
        if new_password != confirm_password:
            st.error("Passwords don't match"); return
        is_valid_pass, pass_msg = valid_password(new_password)
        if not is_valid_pass: st.error(pass_msg); return
        if check_password_reused(st.session_state.reset_email, new_password):
            st.error("Cannot reuse any of your last 5 passwords"); return
        update_password(st.session_state.reset_email, new_password)
        st.success("Password updated successfully!")
        time.sleep(1.5)
        st.session_state.page         = "login"
        st.session_state.reset_email  = None
        st.session_state.otp_verified = False
        st.session_state.reset_method = None
        st.session_state.otp_sent     = False
        st.rerun()

# ================= MAIN ROUTING WITH SIDEBAR =================
if st.session_state.token:
    is_admin = st.session_state.role == "admin"
    username = st.session_state.username

    with st.sidebar:
        st.markdown("""
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem; padding: 0 10px;">
                <div style="width:28px;height:28px;border-radius:6px;background:linear-gradient(135deg, #4F8BF9, #3672e0);display:flex;align-items:center;justify-content:center;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" style="width:16px;height:16px;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                </div>
                <span style="color:#fff;font-weight:600;font-size:1.1rem;letter-spacing:-0.02em;">PolicyNav</span>
            </div>
        """, unsafe_allow_html=True)
        
        if is_admin:
            st.markdown('<div style="padding-left:10px; margin-bottom:1rem;"><span class="admin-badge">ADMIN</span></div>', unsafe_allow_html=True)
            
            st.markdown('<div class="menu-label">Menu</div>', unsafe_allow_html=True)
            if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.menu_option == "Dashboard" else "secondary"):
                st.session_state.menu_option = "Dashboard"; st.rerun()
            if st.button("👥 Users", use_container_width=True, type="primary" if st.session_state.menu_option == "Users" else "secondary"):
                st.session_state.menu_option = "Users"; st.rerun()
        else:
            st.markdown('<div class="menu-label">Tools</div>', unsafe_allow_html=True)
            if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.menu_option == "Dashboard" else "secondary"):
                st.session_state.menu_option = "Dashboard"; st.rerun()
            if st.button("📖 Readability Analyzer", use_container_width=True, type="primary" if st.session_state.menu_option == "Readability" else "secondary"):
                st.session_state.menu_option = "Readability"; st.rerun()

        # This transparent spacer will push the elements below it down toward the bottom of the sidebar
        st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

        if st.button("🚪 Log out", key="logout_btn", use_container_width=True):
            st.session_state.token        = None
            st.session_state.page         = "login"
            st.session_state.username     = None
            st.session_state.role         = "user"
            st.session_state.menu_option  = "Dashboard"
            st.rerun()

        # Simple Profile Text - NO LOGO, NO PLAN 
        st.markdown(f"""
        <div class="sidebar-bottom-profile">
            <div class="profile-name">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;margin-right:8px;vertical-align:middle;">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
                {username}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Main content area
    if is_admin:
        if st.session_state.menu_option == "Dashboard":
            total, blocked, active = get_user_stats()
            st.markdown('<h1 class="page-title">Admin Dashboard</h1>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="stat-card"><p class="stat-number">{total}</p><p class="stat-label">Total Users</p></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="stat-card"><p class="stat-number" style="color:#10b981">{active}</p><p class="stat-label">Active Users</p></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="stat-card"><p class="stat-number" style="color:#ef4444">{blocked}</p><p class="stat-label">Blocked Users</p></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Navigate to **👥 Users** to manage user accounts.")
        elif st.session_state.menu_option == "Users":
            admin_dashboard_page()
    else:
        if st.session_state.menu_option == "Dashboard":
            dashboard_page(st.session_state.username)
        else:
            readability_page()

else:
    if st.session_state.page == "signup":
        signup()
    elif st.session_state.page == "forgot":
        forgot_password()
    elif st.session_state.page == "admin_login":
        admin_login()
    else:
        login()
