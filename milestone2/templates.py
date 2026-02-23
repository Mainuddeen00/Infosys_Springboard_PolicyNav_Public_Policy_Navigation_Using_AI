%%writefile templates.py
class Templates:

    @staticmethod
    def logo():
        return """
        <div class="logo-container">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>
            <div class="logo-text">PolicyNav</div>
            <div class="logo-subtext">Secure Access Management</div>
        </div>
        """

    @staticmethod
    def divider():
        return '<div class="divider"></div>'

    @staticmethod
    def info_box(text):
        return f'<div class="info-box">{text}</div>'

    @staticmethod
    def welcome_message(username):
        return f"""
        <div class="welcome-text">
            Welcome, <span class="username-highlight">{username}</span>!
        </div>
        """
print("templates.py created successfully!")
