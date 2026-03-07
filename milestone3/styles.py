%%writefile styles.py
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    /* ===================== GLOBAL ===================== */
    .stApp, p, h1, h2, h3, h4, h5, h6, span, div, input, button {
        font-family: 'Inter', sans-serif;
    }

    span.material-symbols-rounded,
    i.material-icons,
    [data-testid="collapsedControl"] span,
    [data-testid="baseButton-header"] span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
    }

    /* Gemini-style Dark Backgrounds */
    .stApp { background: #131314 !important; }
    .main  { background: #131314 !important; }

    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header { background: transparent !important; }

    /* ===================== SIDEBAR ===================== */
    section[data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #444746 !important;
    }

    section[data-testid="stSidebar"] .stScrollableContainer {
        padding: 1.5rem 0.8rem !important;
    }

    button[data-testid="collapsedControl"] {
        color: #c4c7c5 !important;
        background-color: transparent !important;
        border: none !important;
        transition: background 0.2s ease !important;
        padding: 0.5rem !important;
    }

    button[data-testid="collapsedControl"]:hover {
        background-color: #282a2c !important;
        border-radius: 8px !important;
    }

    .sidebar-spacer { min-height: 45vh; }

    .menu-label {
        color: #8e918f;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.5rem 0.8rem;
        margin-top: 0.5rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: #c4c7c5 !important;
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
        transition: background 0.15s ease, color 0.15s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #282a2c !important;
        color: #e3e3e3 !important;
    }

    /* Selected state */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #004a77 !important;
        color: #c2e7ff !important;
        font-weight: 500 !important;
    }

    /* Clean Sidebar User Profile block */
    .sidebar-bottom-profile {
        display: flex;
        align-items: center;
        padding: 12px 14px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.2s;
        border-top: 1px solid #444746;
        margin-top: 0.5rem;
    }

    .sidebar-bottom-profile:hover {
        background: #282a2c;
    }

    .profile-name {
        color: #e3e3e3;
        font-size: 0.95rem;
        font-weight: 500;
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
        display: flex;
        align-items: center;
    }

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
        background: #1e1f20;
        border: 1px solid #444746;
        border-radius: 12px;
        margin-bottom: 0.8rem;
    }

    .logo-icon svg {
        width: 2rem;
        height: 2rem;
        color: #a8c7fa;
    }

    .logo-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #e3e3e3;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .logo-subtext {
        color: #8e918f;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin: 0;
    }

    /* ===================== PAGE TITLE ===================== */
    .page-title {
        font-size: 1.8rem;
        font-weight: 500;
        color: #e3e3e3;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
    }

    .page-subtitle {
        color: #8e918f;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* ===================== INPUTS ===================== */
    .stTextInput > label,
    .stSelectbox > label {
        color: #c4c7c5 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.4rem !important;
    }

    .stTextInput > div > div > input {
        background: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
        color: #e3e3e3 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #a8c7fa !important;
        box-shadow: none !important;
        background: #282a2c !important;
    }

    /* ===================== BUTTONS ===================== */
    .main .stButton > button {
        background: #a8c7fa !important;
        color: #062e6f !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin: 0.3rem 0 !important;
        transition: opacity 0.2s ease !important;
        box-shadow: none !important;
    }

    .main .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }

    .main .stButton > button[kind="secondary"] {
        background: #1e1f20 !important;
        color: #a8c7fa !important;
        border: 1px solid #444746 !important;
    }

    .main .stButton > button[kind="secondary"]:hover {
        background: #282a2c !important;
        border-color: #a8c7fa !important;
        transform: none !important;
    }

    /* ===================== ALERTS ===================== */
    .stAlert {
        background: #1e1f20 !important;
        border: 1px solid #444746 !important;
        border-radius: 8px !important;
        color: #e3e3e3 !important;
    }

    /* ===================== ADMIN BADGE ===================== */
    .admin-badge {
        background: #004a77;
        color: #c2e7ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        display: inline-block;
    }

    /* ===================== DASHBOARD STAT CARDS ===================== */
    .stat-card {
        background: #1e1f20;
        border: 1px solid #444746;
        border-radius: 12px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }

    .stat-number {
        font-size: 2.2rem;
        font-weight: 500;
        color: #e3e3e3;
        margin: 0;
        letter-spacing: -0.04em;
        font-family: 'DM Mono', monospace !important;
    }

    .stat-label {
        color: #8e918f;
        font-size: 0.75rem;
        margin: 0.3rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* ===================== READABILITY METRIC CARDS ===================== */
    .metric-card {
        background: #1e1f20;
        border: 1px solid #444746;
        border-radius: 12px;
        padding: 1.4rem;
        position: relative;
    }

    .metric-title {
        color: #8e918f;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
        letter-spacing: 0.05em;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 500;
        color: #e3e3e3;
        font-family: 'DM Mono', monospace !important;
        margin: 0.5rem 0 0.8rem 0;
    }

    .metric-bar-track {
        height: 4px;
        background: #282a2c;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

    .metric-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 1s ease;
    }

    .metric-interpretation {
        font-size: 0.75rem;
        color: #c4c7c5;
        margin: 0;
    }

    /* Level Banner */
    .level-banner {
        background: #1e1f20;
        border: 1px solid #444746;
        border-radius: 12px;
        padding: 1.8rem 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .level-icon {
        width: 56px; height: 56px;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem;
    }

    .level-title { font-size: 1.3rem; font-weight: 500; color: #e3e3e3; margin: 0 0 0.2rem 0; }
    .level-desc { font-size: 0.82rem; color: #8e918f; margin: 0; }
    .level-grade { margin-left: auto; text-align: center; }
    .level-grade-num { font-size: 2.4rem; font-weight: 500; font-family: 'DM Mono', monospace !important; color: #e3e3e3; margin: 0; line-height: 1; }
    .level-grade-label { font-size: 0.72rem; color: #8e918f; text-transform: uppercase; letter-spacing: 0.05em; }

    /* Text Stat Pills */
    .stat-row { display: flex; gap: 0.8rem; margin-top: 1rem; flex-wrap: wrap; }
    .stat-pill { background: #1e1f20; border: 1px solid #444746; border-radius: 10px; padding: 0.8rem 1.2rem; flex: 1; min-width: 100px; text-align: center; }
    .stat-pill-value { font-size: 1.4rem; font-weight: 500; color: #e3e3e3; font-family: 'DM Mono', monospace !important; display: block; }
    .stat-pill-label { font-size: 0.7rem; color: #8e918f; text-transform: uppercase; font-weight: 500; letter-spacing: 0.05em;}

    /* Tooltips */
    .tooltip-wrap { position: relative; display: inline-block; cursor: help; }
    .tooltip-icon { width: 14px; height: 14px; background: #282a2c; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.6rem; color: #8e918f; }
    .tooltip-box { visibility: hidden; opacity: 0; background: #282a2c; border: 1px solid #444746; border-radius: 8px; padding: 0.8rem 1rem; width: 220px; position: absolute; bottom: 130%; left: 50%; transform: translateX(-50%); z-index: 9999; box-shadow: 0 4px 12px rgba(0,0,0,0.3); pointer-events: none; }
    .tooltip-wrap:hover .tooltip-box { visibility: visible; opacity: 1; }
    .tooltip-box p { color: #c4c7c5; font-size: 0.78rem; margin: 0; line-height: 1.5; text-transform: none; font-weight: 400; }
    .tooltip-box strong { color: #e3e3e3; display: block; margin-bottom: 0.3rem; font-size: 0.8rem; text-transform: none; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #444746 !important; border-radius: 0 !important; padding: 0 !important; }
    .stTabs [data-baseweb="tab"] { background: transparent !important; color: #8e918f !important; border-radius: 0 !important; padding: 0.8rem 1rem !important; border: none !important; }
    .stTabs [aria-selected="true"] { background: transparent !important; color: #a8c7fa !important; border-bottom: 2px solid #a8c7fa !important; }

    /* File Uploader */
    .stFileUploader > div { background: #1e1f20 !important; border: 1px dashed #444746 !important; border-radius: 8px !important; }

    /* Text Area */
    .stTextArea textarea { background: #1e1f20 !important; border: 1px solid #444746 !important; border-radius: 8px !important; color: #e3e3e3 !important; }
    .stTextArea textarea:focus { border-color: #a8c7fa !important; box-shadow: none !important; }
</style>
"""
print("styles.py created successfully!")
