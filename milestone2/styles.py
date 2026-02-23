%%writefile styles.py
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* ===================== GLOBAL ===================== */
    /* Target only specific tags so we don't accidentally break Streamlit's Material icons */
    .stApp, p, h1, h2, h3, h4, h5, h6, span, div, input, button {
        font-family: 'DM Sans', sans-serif;
    }

    /* Force Streamlit's internal icons to render correctly! */
    span.material-symbols-rounded, 
    i.material-icons,
    [data-testid="collapsedControl"] span,
    [data-testid="baseButton-header"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    .stApp { background: #212121 !important; }
    .main  { background: #212121 !important; }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    
    /* Make the top header transparent instead of completely hidden so the toggle button stays visible! */
    header { background: transparent !important; }

    /* ===================== SIDEBAR (ChatGPT Style) ===================== */
    section[data-testid="stSidebar"] {
        background-color: #171717 !important; 
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* Target the container INSIDE the sidebar to arrange items */
    section[data-testid="stSidebar"] .stScrollableContainer {
        padding: 1.5rem 0.8rem !important;
    }

    /* Style Streamlit's default collapse button to make it visible against the dark background */
    button[data-testid="collapsedControl"] {
        color: #ececf1 !important;
        background-color: transparent !important;
        border: none !important;
        transition: background 0.2s ease !important;
        padding: 0.5rem !important;
    }
    
    button[data-testid="collapsedControl"]:hover {
        background-color: #2f2f2f !important;
        border-radius: 8px !important;
    }

    /* Push bottom profile to end using empty space */
    .sidebar-spacer {
        min-height: 45vh; 
    }

    /* Menu label */
    .menu-label {
        color: #8e8ea0;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.5rem 0.8rem;
        margin-top: 0.5rem;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #ececf1 !important;
        font-size: 0.9rem !important;
        padding: 0.65rem 0.8rem !important;
        font-weight: 400 !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: none !important;
        margin: 2px 0 !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        transition: background 0.15s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #202123 !important;
    }

    /* Selected state */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #202123 !important;
        font-weight: 500 !important;
    }

    /* Clean Sidebar User Profile block (NO Avatar) */
    .sidebar-bottom-profile {
        display: flex;
        align-items: center;
        padding: 12px 14px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 0.5rem;
    }

    .sidebar-bottom-profile:hover {
        background: #202123;
    }

    .profile-name {
        color: #ececf1;
        font-size: 0.95rem;
        font-weight: 500;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
        display: flex;
        align-items: center;
    }

    /* main area offset */
    .main .block-container {
        padding: 2.5rem 3rem !important;
        max-width: 100% !important;
    }

    /* ===================== LOGO ===================== */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
    }

    .logo-icon {
        display: inline-flex;
        padding: 0.7rem;
        background: linear-gradient(135deg, #1a2540, #0f1829);
        border: 1px solid #2a3d5c;
        border-radius: 14px;
        margin-bottom: 0.8rem;
        box-shadow: 0 0 20px rgba(79,139,249,0.15);
    }

    .logo-icon svg {
        width: 2rem;
        height: 2rem;
        color: #4F8BF9;
    }

    .logo-text {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .logo-subtext {
        color: #4a5a72;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin: 0;
    }

    /* ===================== PAGE TITLE ===================== */
    .page-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
    }

    .page-subtitle {
        color: #8e8ea0;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* ===================== INPUTS ===================== */
    .stTextInput > label,
    .stSelectbox > label {
        color: #8e8ea0 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.4rem !important;
    }

    .stTextInput > div > div > input {
        background: #2f2f2f !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        color: #ececf1 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #4F8BF9 !important;
        box-shadow: 0 0 0 1px #4F8BF9 !important;
        background: #3a3a3a !important;
    }

    /* ===================== BUTTONS ===================== */
    .main .stButton > button {
        background: linear-gradient(135deg, #4F8BF9, #3672e0) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin: 0.3rem 0 !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(79,139,249,0.25) !important;
    }

    .main .stButton > button:hover {
        background: linear-gradient(135deg, #6b9ffa, #4F8BF9) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(79,139,249,0.35) !important;
    }

    .main .stButton > button[kind="secondary"] {
        background: #2f2f2f !important;
        color: #ececf1 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        box-shadow: none !important;
    }

    .main .stButton > button[kind="secondary"]:hover {
        background: #3a3a3a !important;
        border-color: rgba(255,255,255,0.2) !important;
        transform: none !important;
    }

    /* ===================== ALERTS ===================== */
    .stAlert {
        background: #2f2f2f !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: #ececf1 !important;
    }

    /* ===================== ADMIN BADGE ===================== */
    .admin-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #1a1a1a;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: inline-block;
    }

    /* ===================== DASHBOARD STAT CARDS ===================== */
    .stat-card {
        background: #2f2f2f;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4F8BF9;
        margin: 0;
        letter-spacing: -0.04em;
        font-family: 'DM Mono', monospace !important;
    }

    .stat-label {
        color: #8e8ea0;
        font-size: 0.75rem;
        margin: 0.3rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }

    /* ===================== ACTIVITY / QUICK ACTIONS ===================== */
    .activity-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1.2rem 1.5rem;
        background: #2f2f2f;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }

    .activity-item:hover { 
        background: #3a3a3a; 
        transform: translateX(4px);
    }

    .activity-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .activity-text { color: #ececf1; font-size: 0.95rem; font-weight: 500; flex: 1; }
    .activity-time { color: #4F8BF9; font-size: 1rem; font-weight: 700; }

    /* ===================== READABILITY METRIC CARDS ===================== */
    .metric-card {
        background: #2f2f2f;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        padding: 1.4rem;
        position: relative;
    }

    .metric-title {
        color: #8e8ea0;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        font-family: 'DM Mono', monospace !important;
        margin: 0.5rem 0 0.8rem 0;
    }

    .metric-bar-track {
        height: 6px;
        background: #1e2736;
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

    .metric-bar-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 1s ease;
    }

    .metric-interpretation {
        font-size: 0.75rem;
        color: #8e8ea0;
        margin: 0;
    }

    /* Level Banner */
    .level-banner {
        background: #2f2f2f;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .level-icon {
        width: 56px; height: 56px;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem;
    }

    .level-title { font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0 0 0.2rem 0; }
    .level-desc { font-size: 0.82rem; color: #8e8ea0; margin: 0; }
    .level-grade { margin-left: auto; text-align: center; }
    .level-grade-num { font-size: 2.4rem; font-weight: 700; font-family: 'DM Mono', monospace !important; color: #ffffff; margin: 0; line-height: 1; }
    .level-grade-label { font-size: 0.72rem; color: #8e8ea0; text-transform: uppercase; }

    /* Text Stat Pills */
    .stat-row { display: flex; gap: 0.8rem; margin-top: 1rem; flex-wrap: wrap; }
    .stat-pill { background: #2f2f2f; border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 0.8rem 1.2rem; flex: 1; min-width: 100px; text-align: center; }
    .stat-pill-value { font-size: 1.4rem; font-weight: 700; color: #4F8BF9; font-family: 'DM Mono', monospace !important; display: block; }
    .stat-pill-label { font-size: 0.7rem; color: #8e8ea0; text-transform: uppercase; font-weight: 500; }

    /* Tooltips */
    .tooltip-wrap { position: relative; display: inline-block; cursor: help; }
    .tooltip-icon { width: 14px; height: 14px; background: #3a3a3a; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; color: #ececf1; }
    .tooltip-box { visibility: hidden; opacity: 0; background: #171717; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 0.8rem 1rem; width: 220px; position: absolute; bottom: 130%; left: 50%; transform: translateX(-50%); z-index: 9999; box-shadow: 0 10px 30px rgba(0,0,0,0.5); pointer-events: none; }
    .tooltip-wrap:hover .tooltip-box { visibility: visible; opacity: 1; }
    .tooltip-box p { color: #8e8ea0; font-size: 0.78rem; margin: 0; line-height: 1.5; }
    .tooltip-box strong { color: #ececf1; display: block; margin-bottom: 0.3rem; font-size: 0.8rem; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: #2f2f2f !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 10px !important; padding: 4px !important; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; color: #8e8ea0 !important; border-radius: 7px !important; padding: 0.5rem 1rem !important; border: none !important; }
    .stTabs [aria-selected="true"] { background: #3a3a3a !important; color: #ececf1 !important; }

    /* File Uploader */
    .stFileUploader > div { background: #2f2f2f !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 10px !important; }

    /* Text Area */
    .stTextArea textarea { background: #2f2f2f !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 10px !important; color: #ececf1 !important; }
    .stTextArea textarea:focus { border-color: #4F8BF9 !important; }
</style>
"""
print("styles.py created successfully!")
