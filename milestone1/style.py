%%writefile styles.py
CSS = """
<style>
    /* Global Styles */
    .stApp {
        background: #0E1117;
    }
    
    .main {
        background: #0E1117;
    }
    
    /* Main Container */
    .main-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: transparent;
    }
    
    /* Logo Container */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo-icon {
        display: inline-flex;
        padding: 0.75rem;
        background: #1e2530;
        border: 1px solid #2e3642;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon svg {
        width: 2.5rem;
        height: 2.5rem;
        color: #4F8BF9;
    }
    
    .logo-text {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .logo-subtext {
        color: #8b9bb4;
        font-size: 0.95rem;
    }
    
    /* Headers */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Input Fields */
    .stTextInput {
        margin-bottom: 1.2rem;
    }
    
    .stTextInput > label {
        color: #d1d5db !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.3rem !important;
    }
    
    .stTextInput > div > div > input {
        background: #11151c !important;
        border: 1px solid #2e3642 !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1rem !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4F8BF9 !important;
        box-shadow: 0 0 0 2px rgba(79, 139, 249, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
    }
    
    /* Select Box */
    .stSelectbox {
        margin-bottom: 1.2rem;
    }
    
    .stSelectbox > label {
        color: #d1d5db !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        margin-bottom: 0.3rem !important;
    }
    
    .stSelectbox > div > div > select {
        background: #11151c !important;
        border: 1px solid #2e3642 !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1rem !important;
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #4F8BF9 !important;
        color: white !important;
        border: none !important;
        border-radius: 0.5rem !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }
    
    .stButton > button:hover {
        background: #3672e0 !important;
    }
    
    /* Link Buttons */
    .link-button > button {
        background: transparent !important;
        color: #4F8BF9 !important;
        border: 1px solid #4F8BF9 !important;
        box-shadow: none !important;
    }
    
    .link-button > button:hover {
        background: rgba(79, 139, 249, 0.1) !important;
    }
    
    /* Info Box */
    .info-box {
        background: #11151c;
        border: 1px solid #2e3642;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #4F8BF9;
        text-align: center;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: #2e3642;
        margin: 1.5rem 0;
    }
    
    /* Messages */
    .stAlert {
        background: #1e2530 !important;
        border: 1px solid #2e3642 !important;
        border-radius: 0.5rem !important;
        color: #e5e7eb !important;
    }
    
    .stAlert.success {
        border-left: 4px solid #10b981 !important;
    }
    
    .stAlert.error {
        border-left: 4px solid #ef4444 !important;
    }
    
    /* Dashboard */
    .dashboard-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        background: transparent;
        text-align: center;
    }
    
    .welcome-text {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .username-highlight {
        color: #4F8BF9;
        font-weight: 700;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
