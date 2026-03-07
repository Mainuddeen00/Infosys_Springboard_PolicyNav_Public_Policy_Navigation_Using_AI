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
import streamlit.components.v1 as components

# --- AI IMPORTS ---
import pickle
import faiss
import spacy
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pyvis.network import Network
import wikipedia

# ================= LOAD SECRETS =================
EMAIL_ADDRESS = os.environ.get('EMAIL_ID', 'your_email@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD', 'your_app_password')
SECRET_KEY = os.environ.get('JWT_SECRET', 'fallback-secret-key-change-me')
ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL', 'admin@policynav.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')

# ================= PAGE CONFIG =================
st.set_page_config(page_title="PolicyNav", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

# 👇 NEW: Professional, Vibrant SaaS Sidebar CSS (No Emojis) 👇
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0b0f19;
}
[data-testid="stSidebar"] .menu-label {
    color: #60a5fa;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 35px 0 15px 15px;
    font-weight: 700;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 5px;
}
[data-testid="stSidebar"] .stButton button {
    width: 90%;
    margin: 5px auto;
    border-radius: 10px;
    border: 1px solid transparent;
    text-align: left;
    justify-content: flex-start;
    padding: 14px 20px;
    font-weight: 500;
    color: #94a3b8;
    background-color: transparent;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
[data-testid="stSidebar"] .stButton button p {
    font-size: 1.1rem;
}
/* Hover Effect: Slide and Glow */
[data-testid="stSidebar"] .stButton button:hover {
    background-color: #1e293b;
    color: #ffffff;
    transform: translateX(8px);
    border-left: 5px solid #3b82f6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
/* Active Tool Style */
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
    color: #ffffff !important;
    font-weight: 600;
    border-left: 5px solid #60a5fa;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ================= AI MODEL CACHING =================
@st.cache_resource
def load_data_and_models():
    index_path = "/content/drive/MyDrive/PolicyNav/policy_vector_db.index"
    chunks_path = "/content/drive/MyDrive/PolicyNav/chunks.pkl"
    if os.path.exists(index_path) and os.path.exists(chunks_path):
        index = faiss.read_index(index_path)
        with open(chunks_path, "rb") as f: chunks = pickle.load(f)
    else:
        index, chunks = None, [{"source": "No Data", "text": "Run PDF processor first."}]
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    t_tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
    t_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M", device_map="auto")
    s_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    s_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base", device_map="auto")
    nlp = spacy.load("en_core_web_sm")
    return index, chunks, embed_model, t_tokenizer, t_model, s_tokenizer, s_model, nlp

# ================= AI HELPER FUNCTIONS =================
LANG_CODES = {"English": "eng_Latn", "Hindi": "hin_Deva", "Tamil": "tam_Taml", "Telugu": "tel_Telu", "Kannada": "kan_Knda", "Marathi": "mar_Deva", "Bengali": "ben_Beng", "Malayalam": "mal_Mlym", "Gujarati": "guj_Gujr", "Urdu": "urd_Arab"}

def translate_fast(text, source_lang, target_lang, t_tokenizer, t_model):
    if source_lang == target_lang: return text
    t_tokenizer.src_lang = LANG_CODES.get(source_lang, "eng_Latn")
    inputs = t_tokenizer(text, return_tensors="pt", truncation=True).to(t_model.device)
    tgt_id = t_tokenizer.convert_tokens_to_ids(LANG_CODES.get(target_lang, "eng_Latn"))
    outputs = t_model.generate(**inputs, forced_bos_token_id=tgt_id, max_length=512)
    return t_tokenizer.decode(outputs[0], skip_special_tokens=True)

def search_policy(query, index, chunks, embed_model, top_k=5):
    if not index: return ["No database found."]
    query_vector = embed_model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    return [chunks[i]["text"] for i in indices[0]]

def generate_knowledge_graph(chunks_subset, nlp):
    net = Network(height="450px", width="100%", bgcolor="#131314", font_color="#e3e3e3", notebook=False)
    for chunk in chunks_subset:
        filename = chunk["source"]
        doc = nlp(chunk["text"])
        net.add_node(filename, label=filename, color="#a8c7fa", size=20)
        for ent in doc.ents:
            if ent.label_ in ["ORG", "GPE", "DATE"]:
                net.add_node(ent.text, label=ent.text, color="#c4c7c5", size=12)
                net.add_edge(filename, ent.text, title="mentions")
    net.save_graph("policy_graph.html")

def global_web_research(query):
    results = []
    try:
        search_results = wikipedia.search(query, results=3)
        for title in search_results:
            summary = wikipedia.summary(title, sentences=2, auto_suggest=False)
            url = wikipedia.page(title, auto_suggest=False).url
            results.append({"title": title, "body": summary, "href": url})
    except:
        results.append({"title": "Notice", "body": "Could not fetch results.", "href": ""})
    return results

# ================= AUTH & DB CONFIG =================
ALGORITHM, TOKEN_EXPIRE_MINUTES, MAX_LOGIN_ATTEMPTS, LOCKOUT_TIME, OTP_EXPIRY_MINUTES = "HS256", 30, 3, 300, 10
DB_PATH = "/content/drive/MyDrive/PolicyNav/users.db"
conn   = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, security_question TEXT NOT NULL, security_answer TEXT NOT NULL, created_at TEXT, is_blocked INTEGER DEFAULT 0)""")
try: cursor.execute("ALTER TABLE users ADD COLUMN is_blocked INTEGER DEFAULT 0"); conn.commit()
except: pass
cursor.execute("""CREATE TABLE IF NOT EXISTS password_history (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, password TEXT NOT NULL, set_at TEXT, FOREIGN KEY(email) REFERENCES users(email))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS login_attempts (email TEXT PRIMARY KEY, attempts INTEGER DEFAULT 0, last_attempt REAL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS otp_requests (email TEXT PRIMARY KEY, otp TEXT, expires_at REAL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS user_activity (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, action_type TEXT, details TEXT, timestamp TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, rating INTEGER, comments TEXT, timestamp TEXT)""")
try: cursor.execute("ALTER TABLE user_activity ADD COLUMN prompt TEXT"); conn.commit()
except: pass
try: cursor.execute("ALTER TABLE user_activity ADD COLUMN response TEXT"); conn.commit()
except: pass
conn.commit()

# ================= UTILS & VALIDS =================
def _get_timestamp(): return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()
def create_token(email, username, role="user"): return jwt.encode({"sub": email, "username": username, "role": role, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)}, SECRET_KEY, algorithm=ALGORITHM)
def valid_email(email): return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# ================= DB LOGIC =================
def log_activity(email, action_type, details, prompt="", response=""):
    cursor.execute("INSERT INTO user_activity (email, action_type, details, prompt, response, timestamp) VALUES (?, ?, ?, ?, ?, ?)", (email, action_type, details, prompt, response, _get_timestamp())); conn.commit()

def get_user_history(email):
    cursor.execute("SELECT action_type, details, prompt, response, timestamp FROM user_activity WHERE email = ? AND action_type != 'System' ORDER BY id DESC", (email,))
    return cursor.fetchall()

def submit_feedback(email, rating, comments):
    cursor.execute("INSERT INTO feedback (email, rating, comments, timestamp) VALUES (?, ?, ?, ?)", (email, rating, comments, _get_timestamp())); conn.commit()
def get_all_feedback(): cursor.execute("SELECT email, rating, comments, timestamp FROM feedback ORDER BY id DESC"); return cursor.fetchall()
def get_login_attempts(email): cursor.execute("SELECT attempts, last_attempt FROM login_attempts WHERE email = ?", (email,)); data = cursor.fetchone(); return data if data else (0, 0)
def increment_login_attempts(email): attempts, _ = get_login_attempts(email); cursor.execute("INSERT OR REPLACE INTO login_attempts (email, attempts, last_attempt) VALUES (?, ?, ?)", (email, attempts + 1, time.time())); conn.commit()
def reset_login_attempts(email): cursor.execute("DELETE FROM login_attempts WHERE email = ?", (email,)); conn.commit()
def is_rate_limited(email):
    attempts, last_attempt = get_login_attempts(email)
    if attempts >= MAX_LOGIN_ATTEMPTS:
        if time.time() - last_attempt < LOCKOUT_TIME: return True, LOCKOUT_TIME - (time.time() - last_attempt)
        else: reset_login_attempts(email)
    return False, 0
def register_user(username, email, password, security_question, security_answer):
    try:
        now, hashed_pass, hashed_answer = _get_timestamp(), hash_password(password), hash_password(security_answer.strip())
        cursor.execute("INSERT INTO users (username, email, password, security_question, security_answer, created_at) VALUES (?, ?, ?, ?, ?, ?)", (username, email, hashed_pass, security_question, hashed_answer, now))
        cursor.execute("INSERT INTO password_history (email, password, set_at) VALUES (?, ?, ?)", (email, hashed_pass, now)); conn.commit(); return True
    except sqlite3.IntegrityError: return False
def authenticate_user(email, password):
    is_limited, _ = is_rate_limited(email)
    if is_limited: return False, "locked"
    cursor.execute("SELECT username, password, is_blocked FROM users WHERE email = ?", (email,)); user = cursor.fetchone()
    if user:
        if user[2] == 1: return False, "blocked"
        if user[1] == hash_password(password): reset_login_attempts(email); return True, user[0]
    increment_login_attempts(email); return False, None
def authenticate_admin(email, password): return email == ADMIN_EMAIL and password == ADMIN_PASSWORD
def check_user_exists(email): cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,)); return cursor.fetchone() is not None
def get_user_details(email): cursor.execute("SELECT username, security_question, security_answer FROM users WHERE email = ?", (email,)); return cursor.fetchone()
def check_password_reused(email, new_password):
    cursor.execute("SELECT password FROM password_history WHERE email = ? ORDER BY id DESC LIMIT 5", (email,)); history = cursor.fetchall(); hashed_new = hash_password(new_password)
    for (stored_hash,) in history:
        if stored_hash == hashed_new: return True
    return False
def update_password(email, new_password):
    hashed, now = hash_password(new_password), _get_timestamp()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email)); cursor.execute("INSERT INTO password_history (email, password, set_at) VALUES (?, ?, ?)", (email, hashed, now)); conn.commit(); reset_login_attempts(email)
def verify_security_answer(email, answer): cursor.execute("SELECT security_answer FROM users WHERE email = ?", (email,)); stored_answer = cursor.fetchone(); return stored_answer and stored_answer[0] == hash_password(answer.strip())
def get_all_users(): cursor.execute("SELECT id, username, email, created_at, is_blocked FROM users ORDER BY id DESC"); return cursor.fetchall()
def block_user(email): cursor.execute("UPDATE users SET is_blocked = 1 WHERE email = ?", (email,)); conn.commit()
def unblock_user(email): cursor.execute("UPDATE users SET is_blocked = 0 WHERE email = ?", (email,)); conn.commit()
def delete_user(email):
    cursor.execute("DELETE FROM users WHERE email = ?", (email,)); cursor.execute("DELETE FROM password_history WHERE email = ?", (email,))
    cursor.execute("DELETE FROM login_attempts WHERE email = ?", (email,)); cursor.execute("DELETE FROM otp_requests WHERE email = ?", (email,))
    cursor.execute("DELETE FROM user_activity WHERE email = ?", (email,)); cursor.execute("DELETE FROM feedback WHERE email = ?", (email,)); conn.commit()
def get_user_stats():
    cursor.execute("SELECT COUNT(*) FROM users"); total = cursor.fetchone()[0]; cursor.execute("SELECT COUNT(*) FROM users WHERE is_blocked = 1"); blocked = cursor.fetchone()[0]
    return total, blocked, total - blocked

def generate_otp(): return f"{secrets.randbelow(1000000):06d}"
def save_otp(email, otp): expires_at = time.time() + (OTP_EXPIRY_MINUTES * 60); cursor.execute("INSERT OR REPLACE INTO otp_requests (email, otp, expires_at) VALUES (?, ?, ?)", (email, otp, expires_at)); conn.commit()
def verify_otp(email, otp):
    cursor.execute("SELECT otp, expires_at FROM otp_requests WHERE email = ?", (email,)); data = cursor.fetchone()
    if data and data[0] == otp and time.time() < data[1]: cursor.execute("DELETE FROM otp_requests WHERE email = ?", (email,)); conn.commit(); return True
    return False
def send_otp_email(to_email, otp):
    try:
        msg = MIMEMultipart(); msg['From'] = f"PolicyNav <{EMAIL_ADDRESS}>"; msg['To'] = to_email; msg['Subject'] = "PolicyNav Password Reset"
        body = f"<html><body><h1 style='color: #e3e3e3; text-align: center;'>{otp}</h1></body></html>"
        msg.attach(MIMEText(body, 'html')); server = smtplib.SMTP('smtp.gmail.com', 587); server.starttls(); server.login(EMAIL_ADDRESS, EMAIL_PASSWORD); server.send_message(msg); server.quit()
        return True, "OTP sent successfully"
    except Exception as e: return False, str(e)

# ================= SESSION =================
_session_defaults = {"page": "login", "token": None, "role": "user", "reset_email": None, "security_question": None, "otp_verified": False, "username": None, "email": None, "menu_option": "Dashboard", "reset_method": None, "otp_sent": False}
for _k, _v in _session_defaults.items():
    if _k not in st.session_state: st.session_state[_k] = _v

def metric_card(label, tooltip_desc, value, bar_pct, bar_color):
    bar_pct_clamped = max(0, min(100, bar_pct))
    return f"""<div class="metric-card"><div class="metric-title">{label}</div><div class="metric-value">{value:.1f}</div><div class="metric-bar-track"><div class="metric-bar-fill" style="width:{bar_pct_clamped}%; background:{bar_color};"></div></div><p class="metric-interpretation">{tooltip_desc}</p></div>"""

# ================= PAGES =================
def dashboard_page(username, chunks):
    now_dt = datetime.datetime.now()
    _, center_col, _ = st.columns([1, 6, 1])
    with center_col:
        st.markdown(f"<div style='margin-bottom: 2rem; margin-top: 2rem; text-align: center;'><p style='color: #a8c7fa; font-size: 0.85rem; margin: 0 0 0.2rem 0; text-transform: uppercase; letter-spacing: 0.05em;'>Welcome back</p><h1 style='margin-bottom: 0.2rem; font-size: 2.5rem; color: #e3e3e3;'>{username}</h1><p style='color: #8e918f; font-size: 0.9rem; margin: 0;'>{now_dt.strftime('%A, %B %d, %Y')}</p></div>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: #e3e3e3; margin-top: 1rem;'>Latest Policy Updates</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8e918f; font-size: 0.9rem; text-align: center; margin-bottom: 1.5rem;'>Hover over the feed to pause scrolling and read.</p>", unsafe_allow_html=True)
        
        unique_srcs = []
        for c in reversed(chunks):
            if c["source"] not in unique_srcs and c["source"] != "No Data":
                unique_srcs.append(c["source"])
            if len(unique_srcs) >= 5: break
        
        cards_html = ""
        if not unique_srcs:
            cards_html = "<div class='policy-card'><p class='policy-title'>No Policies Found</p><p class='policy-desc'>Please process PDFs to populate the database.</p></div>"
        else:
            for src in unique_srcs:
                first_chunk = ""
                for c in chunks:
                    if c["source"] == src:
                        first_chunk = c["text"]
                        break
                title = src.replace(".pdf", "").replace("_", " ").title()
                desc = first_chunk[:130] + "..." if len(first_chunk) > 130 else first_chunk
                cards_html += f"<div class='policy-card'><p class='policy-title'>{title}</p><p class='policy-desc'>{desc}</p><span class='policy-tag'>Recently Added to Database</span></div>"

        # 👇 FIXED: Flattened string to prevent Markdown Code-Block Bug 👇
        ticker_css = "<style>.news-ticker-container {height: 350px; overflow: hidden; background-color: #1e1f20; border-radius: 12px; border: 1px solid #444746; position: relative; padding: 10px 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.4); } .news-scroll {display: flex; flex-direction: column; gap: 15px; animation: scroll-vertical 20s linear infinite; } .news-ticker-container:hover .news-scroll {animation-play-state: paused; } .policy-card {background-color: #131314; padding: 18px; border-radius: 8px; border-left: 5px solid #a8c7fa; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom:10px;} .policy-title {color: #a8c7fa; font-size: 1.15rem; font-weight: 600; margin: 0 0 8px 0; } .policy-desc {color: #e3e3e3; font-size: 0.95rem; margin: 0; line-height: 1.5; } .policy-tag {display: inline-block; background-color: #2e3032; color: #81c995; font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; margin-top: 10px; } @keyframes scroll-vertical {0% { transform: translateY(100%); } 100% { transform: translateY(-100%); } } </style>"
        ticker_html = f"<div class='news-ticker-container'><div class='news-scroll'>{cards_html}</div></div>"
        
        st.markdown(ticker_css + ticker_html, unsafe_allow_html=True)

def signup():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Create Account</h1>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", placeholder="your_username", key="signup_username")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_password")
            security_question = st.selectbox("Security Question", ["What is your pet name?", "What is your mother's maiden name?", "What is your favorite teacher?"], key="signup_question")
        with col2:
            email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")
            security_answer = st.text_input("Security Answer", placeholder="Your answer", key="signup_answer")
        if st.button("Create Account", key="signup_button", use_container_width=True, type="primary"):
            if not all([username, email, password, confirm, security_answer]): st.error("All fields required"); return
            if password != confirm: st.error("Passwords do not match"); return
            if register_user(username, email, password, security_question, security_answer):
                st.success("Account created successfully"); time.sleep(1.5); st.session_state.page = "login"; st.rerun()
            else: st.error("Registration failed or Email exists")
        if st.button("Back to Login", key="back_to_login", use_container_width=True): st.session_state.page = "login"; st.rerun()

def login():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Welcome back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Sign in to your account</p>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        email = st.text_input("Email", placeholder="you@example.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
        if st.button("Sign In", key="login_button", use_container_width=True, type="primary"):
            if not email or not password: st.error("Please enter email and pass both")
            else:
                auth_result, status = authenticate_user(email, password)
                if auth_result:
                    st.session_state.token = create_token(email, status, "user")
                    st.session_state.username = status
                    st.session_state.email = email
                    st.session_state.role = "user"
                    st.session_state.page = "dashboard"
                    log_activity(email, "System", "User logged in successfully")
                    st.rerun()
                else:
                    if status == "locked": st.error("Account locked. Try again later.")
                    elif status == "blocked": st.error("Account blocked by admin.")
                    else: st.error("Invalid credentials")
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Create Account", use_container_width=True): st.session_state.page = "signup"; st.rerun()
        with c2:
            if st.button("Forgot Password", use_container_width=True): st.session_state.page = "forgot"; st.rerun()
        with c3:
            if st.button("Admin", use_container_width=True): st.session_state.page = "admin_login"; st.rerun()

def admin_login():
    st.markdown("<h1 style='text-align:center;'>Admin Access</h1>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        admin_email = st.text_input("Admin Email", key="admin_email")
        admin_pass = st.text_input("Admin Password", type="password", key="admin_pass")
        if st.button("Access Admin Panel", type="primary", use_container_width=True):
            if authenticate_admin(admin_email, admin_pass):
                st.session_state.token = "admin_token"
                st.session_state.username = "Admin"
                st.session_state.email = admin_email
                st.session_state.role = "admin"
                st.session_state.page = "dashboard"
                st.rerun()
            else: st.error("Invalid admin credentials")
        if st.button("Back to User Login", use_container_width=True): st.session_state.page = "login"; st.rerun()

def forgot_password():
    st.markdown(Templates.logo(), unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Reset Password</h1>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        if not st.session_state.reset_email:
            email = st.text_input("Email", placeholder="Your registered email", key="forgot_email")
            st.markdown("<p style='text-align:center; margin:1rem 0 0.5rem; font-size:0.85rem;'>Choose your verification method</p>", unsafe_allow_html=True)
            col_otp, col_sec = st.columns(2)
            with col_otp: otp_btn = st.button("Via OTP Email", use_container_width=True)
            with col_sec: sec_btn = st.button("Via Security Q&A", use_container_width=True)
            if otp_btn or sec_btn:
                if not email: st.error("Please enter your email first")
                elif not check_user_exists(email): st.error("Email not found in our system")
                elif otp_btn:
                    otp = generate_otp(); save_otp(email, otp); success, msg = send_otp_email(email, otp)
                    if success: st.session_state.reset_email = email; st.session_state.reset_method = "otp"; st.success("OTP sent to your email."); time.sleep(1); st.rerun()
                    else: st.error(f"Failed to send OTP: {msg}")
                else: st.session_state.reset_email = email; st.session_state.reset_method = "security"; st.rerun()
        elif st.session_state.reset_method == "otp" and not st.session_state.otp_verified:
            otp_input = st.text_input("Enter OTP", placeholder="6-digit code", max_chars=6)
            if st.button("Verify OTP", type="primary", use_container_width=True):
                if verify_otp(st.session_state.reset_email, otp_input): st.session_state.otp_verified = True; st.success("OTP verified."); st.rerun()
                else: st.error("Invalid or expired OTP")
        elif st.session_state.reset_method == "security" and not st.session_state.otp_verified:
            user_details = get_user_details(st.session_state.reset_email)
            if user_details:
                st.info(f"Question: {user_details[1]}")
                answer = st.text_input("Your Answer", placeholder="Enter your answer")
                if st.button("Verify Answer", type="primary", use_container_width=True):
                    if verify_security_answer(st.session_state.reset_email, answer): st.session_state.otp_verified = True; st.success("Answer verified."); time.sleep(0.8); st.rerun()
                    else: st.error("Incorrect security answer")
        elif st.session_state.otp_verified:
            new_password = st.text_input("New Password", type="password", placeholder="••••••••")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            if st.button("Reset Password", type="primary", use_container_width=True):
                if new_password == confirm_password and not check_password_reused(st.session_state.reset_email, new_password):
                    update_password(st.session_state.reset_email, new_password); st.success("Password updated successfully."); time.sleep(1.5)
                    st.session_state.page = "login"; st.session_state.reset_email = None; st.session_state.otp_verified = False; st.rerun()
                else: st.error("Passwords mismatch or reused old password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Back", use_container_width=True): st.session_state.page = "login"; st.session_state.reset_email = None; st.session_state.otp_verified = False; st.rerun()

# ================= MAIN ROUTING =================
if st.session_state.token:
    is_admin = st.session_state.role == "admin"
    username = st.session_state.username
    if not is_admin:
        with st.spinner("Initializing Workspace..."): index, chunks, embed_model, t_tokenizer, t_model, s_tokenizer, s_model, nlp = load_data_and_models()

    with st.sidebar:
        st.markdown("<div style='display:flex; align-items:center; gap:10px; margin-bottom:2rem; padding: 0 10px;'><div style='width:32px;height:32px;border-radius:8px;background:#3b82f6;display:flex;align-items:center;justify-content:center;'><svg viewBox='0 0 24 24' fill='none' stroke='#ffffff' stroke-width='2' style='width:20px;height:20px;'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/></svg></div><span style='color:#ffffff;font-weight:700;font-size:1.3rem;letter-spacing:-0.02em;'>PolicyNav</span></div>", unsafe_allow_html=True)
        if is_admin:
            st.markdown("<div class='menu-label'>ADMINISTRATION</div>", unsafe_allow_html=True)
            if st.button("System Dashboard", use_container_width=True, type="primary" if st.session_state.menu_option == "Dashboard" else "secondary"): st.session_state.menu_option = "Dashboard"; st.rerun()
        else:
            st.markdown("<div class='menu-label'>AI INTELLIGENCE</div>", unsafe_allow_html=True)
            if st.button("User Dashboard", use_container_width=True, type="primary" if st.session_state.menu_option == "Dashboard" else "secondary"): st.session_state.menu_option = "Dashboard"; st.rerun()
            if st.button("AI Policy Assistant", use_container_width=True, type="primary" if st.session_state.menu_option == "Chat" else "secondary"): st.session_state.menu_option = "Chat"; st.rerun()
            if st.button("AI Policy Summarizer", use_container_width=True, type="primary" if st.session_state.menu_option == "Summarization" else "secondary"): st.session_state.menu_option = "Summarization"; st.rerun()
            if st.button("Entity Knowledge Graph", use_container_width=True, type="primary" if st.session_state.menu_option == "Graph" else "secondary"): st.session_state.menu_option = "Graph"; st.rerun()
            if st.button("Global Web Search", use_container_width=True, type="primary" if st.session_state.menu_option == "Web" else "secondary"): st.session_state.menu_option = "Web"; st.rerun()
            if st.button("Readability Analyzer", use_container_width=True, type="primary" if st.session_state.menu_option == "Readability" else "secondary"): st.session_state.menu_option = "Readability"; st.rerun()
            if st.button("Language Translator", use_container_width=True, type="primary" if st.session_state.menu_option == "Translation" else "secondary"): st.session_state.menu_option = "Translation"; st.rerun()
            st.markdown("<div class='menu-label'>PERSONAL PORTAL</div>", unsafe_allow_html=True)
            if st.button("My Activity History", use_container_width=True, type="primary" if st.session_state.menu_option == "History" else "secondary"): st.session_state.menu_option = "History"; st.rerun()
            if st.button("Submit Feedback", use_container_width=True, type="primary" if st.session_state.menu_option == "Feedback" else "secondary"): st.session_state.menu_option = "Feedback"; st.rerun()
        st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
        if st.button("Log out", key="logout_btn", use_container_width=True):
            log_activity(st.session_state.email, "System", "User logged out")
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()
        st.markdown(f"<div style='padding:20px; border-top:1px solid #1e293b; color:#94a3b8; font-size:0.9rem;'>Logged in as: <br><b style='color:#ffffff;'>{username}</b></div>", unsafe_allow_html=True)

    # --- MAIN CONTENT AREA ROUTING ---
    if is_admin:
        if st.session_state.menu_option == "Dashboard":
            st.markdown("<h2>Admin Control Panel</h2>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Manage Users", "User Feedback"])
            with tab1:
                total, blocked, active = get_user_stats()
                c1, c2, c3 = st.columns(3)
                with c1: st.markdown(f"<div class='clean-card'><p style='font-size:2rem; margin:0; color:#e3e3e3;'>{total}</p><p class='card-meta'>Total Users</p></div>", unsafe_allow_html=True)
                with c2: st.markdown(f"<div class='clean-card'><p style='font-size:2rem; margin:0; color:#a8c7fa;'>{active}</p><p class='card-meta'>Active Users</p></div>", unsafe_allow_html=True)
                with c3: st.markdown(f"<div class='clean-card'><p style='font-size:2rem; margin:0; color:#e3e3e3;'>{blocked}</p><p class='card-meta'>Blocked</p></div>", unsafe_allow_html=True)
                users = get_all_users()
                for uid, uname, uemail, ucreated, ublocked in users:
                    st.markdown(f"<div class='clean-card' style='display:flex; justify-content:space-between; align-items:center; padding:15px;'><span style='color:#e3e3e3;'>{uname} <span style='color:#8e918f;'>({uemail})</span></span></div>", unsafe_allow_html=True)
                    if st.button(f"Delete {uname}", key=f"del_{uid}"): delete_user(uemail); st.success(f"Deleted {uname}"); time.sleep(0.8); st.rerun()
            with tab2:
                feedbacks = get_all_feedback()
                if not feedbacks: st.info("No feedback submitted yet.")
                for email, rating, comments, ts in feedbacks:
                    st.markdown(f"<div class='clean-card'><p class='card-title'>{email} <span style='float:right; color:#8e918f; font-size:0.8rem;'>{ts}</span></p><p style='color:#a8c7fa; margin:5px 0;'>Rating: {rating}/5</p><p class='card-text'>{comments}</p></div>", unsafe_allow_html=True)
    else:
        if st.session_state.menu_option == "Dashboard": dashboard_page(st.session_state.username, chunks)
        elif st.session_state.menu_option == "History":
            st.header("My Activity History")
            history = get_user_history(st.session_state.email)
            if not history: st.info("No activity recorded yet.")
            else:
                for action, details, prompt, response, ts in history:
                    if prompt or response:
                        with st.expander(f"{action} | {ts}"):
                            st.markdown("**Your Prompt / Input:**"); st.info(prompt)
                            st.markdown("**AI Response:**"); st.success(response)
                    else: st.markdown(f"<div class='clean-card'><p class='card-title'>{action} <span style='float:right; color:#8e918f; font-size:0.8rem; font-weight:400;'>{ts}</span></p><p class='card-text'>{details}</p></div>", unsafe_allow_html=True)
        elif st.session_state.menu_option == "Feedback":
            st.header("Submit Feedback")
            st.markdown("<p style='color:#c4c7c5;'>Help us improve PolicyNav. Your feedback is sent directly to our administration team.</p>", unsafe_allow_html=True)
            with st.form("feedback_form"):
                rating = st.slider("Rate your experience (1 = Poor, 5 = Excellent)", 1, 5, 5)
                comments = st.text_area("Any suggestions, feature requests, or bugs to report?", height=150)
                if st.form_submit_button("Submit Feedback", type="primary"):
                    if not comments.strip(): st.error("Please write a comment or suggestion before submitting.")
                    else: submit_feedback(st.session_state.email, rating, comments); st.success("Thank you. Your feedback has been recorded.")
        elif st.session_state.menu_option == "Chat":
            st.header("AI Policy Assistant")
            q = st.text_input("Ask a question about government policies:")
            col1, col2, _ = st.columns([2, 3, 5])
            with col1: submit_btn = st.button("Ask AI", type="primary", use_container_width=True)
            with col2: target_lang = st.selectbox("Output Language", list(LANG_CODES.keys()), key="chat_lang", label_visibility="collapsed")
            if submit_btn and q:
                with st.spinner("Searching..."):
                    eng_q = translate_fast(q, target_lang, "English", t_tokenizer, t_model)
                    context = "\n\n".join(search_policy(eng_q, index, chunks, embed_model))
                    prompt = f"Based on policy context, answer in 2-3 sentences.\n\nContext:\n{context}\n\nQuestion:\n{eng_q}"
                    inputs = s_tokenizer(prompt, return_tensors="pt").to(s_model.device)
                    outputs = s_model.generate(**inputs, max_new_tokens=150)
                    eng_ans = s_tokenizer.decode(outputs[0], skip_special_tokens=True)
                    final_ans = translate_fast(eng_ans, 'English', target_lang, t_tokenizer, t_model)
                    st.markdown(f"<div class='clean-card'><p class='card-title'>Answer</p><p class='card-text'>{final_ans}</p></div>", unsafe_allow_html=True)
                log_activity(st.session_state.email, "Chat", f"Queried: '{q}'", prompt=q, response=final_ans)
        elif st.session_state.menu_option == "Summarization":
            st.header("AI Policy Summarizer")
            text_to_summarize = st.text_area("Paste policy document text here:", height=250)
            col1, col2, _ = st.columns([2, 3, 5])
            with col1: sum_btn = st.button("Generate Summary", type="primary", use_container_width=True)
            with col2: target_lang = st.selectbox("Output Language", list(LANG_CODES.keys()), key="sum_lang", label_visibility="collapsed")
            if sum_btn:
                if len(text_to_summarize.strip()) < 50: st.error("Enter at least 50 characters.")
                else:
                    with st.spinner("Processing..."):
                        prompt = f"Summarize in 3-4 sentences.\n\nText: {text_to_summarize[:2000]}"
                        inputs = s_tokenizer(prompt, return_tensors="pt", truncation=True).to(s_model.device)
                        outputs = s_model.generate(**inputs, max_new_tokens=250, min_length=50, num_beams=2, early_stopping=True)
                        eng_summary = s_tokenizer.decode(outputs[0], skip_special_tokens=True)
                        final_summary = translate_fast(eng_summary, "English", target_lang, t_tokenizer, t_model)
                        st.markdown(f"<div class='clean-card'><p class='card-title'>Summary Result</p><p class='card-text'>{final_summary}</p></div>", unsafe_allow_html=True)
                    log_activity(st.session_state.email, "Summarization", f"Summary in {target_lang}", prompt=text_to_summarize, response=final_summary)
        elif st.session_state.menu_option == "Graph":
            st.header("Entity Knowledge Graph")
            if st.button("Generate Graph", type="primary"):
                log_activity(st.session_state.email, "Knowledge Graph", "Rendered graph")
                with st.spinner("Extracting..."): generate_knowledge_graph(chunks[:15], nlp); components.html(open("policy_graph.html", 'r', encoding='utf-8').read(), height=450)
        elif st.session_state.menu_option == "Web":
            st.header("Global Web Search")
            query = st.text_input("Enter research query:")
            if st.button("Search Web", type="primary") and query:
                with st.spinner("Retrieving..."):
                    results = global_web_research(query)
                    for r in results: st.markdown(f"<div class='clean-card'><p class='card-title'>{r['title']}</p><p class='card-text'>{r['body']}</p><a href='{r['href']}' style='color:#a8c7fa; font-size:0.85rem; text-decoration:none;'>Read source document</a></div>", unsafe_allow_html=True)
                log_activity(st.session_state.email, "Web Research", f"Researched: '{query}'", prompt=query, response="\n\n".join([f"**{r['title']}**\n{r['body']}" for r in results]))
        elif st.session_state.menu_option == "Readability":
            st.header("Readability Analyzer")
            tab1, tab2 = st.tabs(["Paste Text", "Upload File"]); text_input = ""
            with tab1: 
                raw_text = st.text_area("Enter text below", height=180, key="read_txt")
                if raw_text: text_input = raw_text
            with tab2:
                uploaded_file = st.file_uploader("Upload file", type=["txt", "pdf"])
                if uploaded_file:
                    if uploaded_file.type == "application/pdf": text_input = "".join([page.extract_text() + "\n" for page in PyPDF2.PdfReader(uploaded_file).pages])
                    else: text_input = uploaded_file.read().decode("utf-8")
            if st.button("Analyze Text", type="primary"):
                if len(text_input.strip()) < 50: st.error("Text too short.")
                else:
                    with st.spinner("Calculating..."):
                        scores = readability.ReadabilityAnalyzer(text_input).get_all_metrics()
                        st.markdown("<br>", unsafe_allow_html=True); c1, c2, c3 = st.columns(3)
                        with c1: st.markdown(metric_card("Flesch Ease", "0-100 score", scores["Flesch Reading Ease"], scores["Flesch Reading Ease"], "#a8c7fa"), unsafe_allow_html=True)
                        with c2: st.markdown(metric_card("Flesch-Kincaid", "Grade level", scores["Flesch-Kincaid Grade"], (scores["Flesch-Kincaid Grade"] / 20) * 100, "#81c995"), unsafe_allow_html=True)
                        with c3: st.markdown(metric_card("SMOG Index", "Education level", scores["SMOG Index"], (scores["SMOG Index"] / 20) * 100, "#f28b82"), unsafe_allow_html=True)
                    log_activity(st.session_state.email, "Readability", "Analyzed metrics", prompt=text_input[:200] + "...", response=f"Flesch Ease: {scores['Flesch Reading Ease']:.1f}")
        elif st.session_state.menu_option == "Translation":
            st.header("Language Translator")
            source_lang = st.selectbox("Detect Source Language:", list(LANG_CODES.keys()), index=0)
            text_to_translate = st.text_area("Paste text to translate:", height=200)
            col1, col2, _ = st.columns([2, 3, 5])
            with col1: trans_btn = st.button("Translate Text", type="primary", use_container_width=True)
            with col2: target_lang = st.selectbox("Output Language", list(LANG_CODES.keys()), key="trans_lang", label_visibility="collapsed")
            if trans_btn:
                if text_to_translate.strip() == "": st.error("Please paste text.")
                else:
                    with st.spinner("Translating..."):
                        result = translate_fast(text_to_translate, source_lang, target_lang, t_tokenizer, t_model)
                        st.markdown(f"<div class='clean-card'><p class='card-title'>Translation</p><p class='card-text'>{result}</p></div>", unsafe_allow_html=True)
                    log_activity(st.session_state.email, "Translation", f"To {target_lang}", prompt=text_to_translate, response=result)
else:
    if st.session_state.page == "signup": signup()
    elif st.session_state.page == "admin_login": admin_login()
    elif st.session_state.page == "forgot": forgot_password()
    else: login()
