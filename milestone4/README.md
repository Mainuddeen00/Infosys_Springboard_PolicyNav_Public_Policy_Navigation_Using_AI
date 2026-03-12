# PolicyNav - Milestone 4: End-to-End Application & Admin Analytics

## Overview
Milestone 4 represents the final integration phase of the Infosys Springboard Internship. This phase elevates the project from a suite of AI tools into a fully managed, enterprise-grade SaaS platform. It introduces a comprehensive **Admin Command Center** for real-time data analytics and a **User Profile** portal for identity and strict security management.

---

## 1. Admin Dashboard (Management & Analytics)
The Admin panel has been engineered as a central command center, equipping administrators with powerful oversight, database management, and reporting capabilities.

### User Control
The system implements strict Role-Based Access Control (RBAC). Administrators can instantly elevate standard accounts to Admin status, granting them full dashboard access. To maintain platform integrity, Admins can manually lock or unlock accounts to mitigate compromised credentials. Furthermore, Admins can permanently delete users, which safely cascades the deletion across all relational database tables (clearing their history, OTPs, and feedback).

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 08 36 PM" src="https://github.com/user-attachments/assets/77b87fee-d069-4d7f-b471-dd7520684e7b" />


### Activity Tracking
A comprehensive auditing module allows Admins to view an aggregated, chronological feed of all user interactions. This tracks exact AI prompts, generated responses, tool usage, and timestamps across the entire platform, providing a transparent view of real-time system engagement and user behavior.

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 08 46 PM" src="https://github.com/user-attachments/assets/fb1defe8-d274-4911-a9e4-2ea5bc3884bc" />


### Data Visualization
Leveraging `pandas` for data manipulation and `plotly.express` for dynamic rendering, the dashboard generates interactive, dark-themed visualizations to provide actionable business intelligence. 
* **Model & Feature Popularity:** Bar charts dynamically track and display which AI tools (e.g., AI Policy Assistant vs. Summarizer) are driving the most user engagement.
* **Language Utilization:** Interactive pie charts map the distribution of regional language outputs, highlighting the platform's linguistic reach and accessibility impact across different demographics.

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 00 PM" src="https://github.com/user-attachments/assets/d96afe62-d249-437f-83cf-047d2a6371fc" />


### Feedback Analysis
To process qualitative data efficiently, the platform automatically aggregates all text-based user comments from the feedback databases. It utilizes the `wordcloud` and `matplotlib` libraries to render a visual sentiment map. This allows administrators to instantly identify recurring themes, highly requested features, and common pain points at a single glance without reading hundreds of individual rows.
<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 11 PM" src="https://github.com/user-attachments/assets/10241c6c-97e9-4755-81da-480955061560" />


### Data Export
For offline analysis and compliance reporting, the system features instant 1-click data extraction. Using Pandas dataframe conversions, administrators can download comprehensive `.csv` files containing the complete user directory, full activity logs, and granular AI tool performance feedback directly to their local machines.

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 29 PM" src="https://github.com/user-attachments/assets/73d123bc-b583-49bc-b486-0088db210c96" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 26 22 PM" src="https://github.com/user-attachments/assets/f2cfc07c-a6cd-44de-8602-0bf68c9683b1" />



---

## 2. User Dashboard & Profile Personalization
The standard user experience has been highly personalized and secured, giving users complete autonomy over their accounts and data.

### Security Settings
Users are empowered to manage their own credentials through a highly secure interface. 
* **Email Updates:** Updating an email address safely cascades the change across all relational database tables (history, feedback, etc.) so no user data is orphaned or lost.
* **Password Management:** Password changes require strict verification of the current password and check the database history to prevent the reuse of recent passwords. Upon a successful password change, the system automatically triggers a forced cache clear and session logout, kicking the user to the login screen to ensure maximum account security.

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 37 PM" src="https://github.com/user-attachments/assets/b9076530-ee43-4ebb-9119-39b371e6d260" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 50 PM" src="https://github.com/user-attachments/assets/27704673-9d08-4de6-9834-2bed4f415bcb" />



### Identity & Avatar (DP) Personalization
To personalize the SaaS experience, users can upload a custom Profile Avatar (PNG/JPG). 
* **Smart Storage:** Instead of relying on complex external cloud storage buckets, the uploaded image is converted directly into a Base64 encoded string and stored natively within the SQLite database.
* **Validation & UI:** The system includes a strict 5MB backend file size validation check. Upon a successful upload, the Base64 string instantly decodes and updates the application's sidebar UI, replacing the default placeholder icon with the user's custom image. 

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 23 PM" src="https://github.com/user-attachments/assets/ab80b983-8fc6-4447-a8aa-ea23daed5369" />

