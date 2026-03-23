# Infosys Springboard
# PolicyNav - Public-Policy-Navigation-Using-AI
AI-Powered Public Policy Navigation and Intelligence Platform
Simplifying complex government policies through multilingual AI, summarization, and intelligent search.
# Links: 
| Category       | Link                                   |
| -------------- | -------------------------------------- |
| Demo Video     | https://drive.google.com/file/d/1iWPSKYKJvN9n7cfZkcAdOkUDFPQ0DH1q/view?usp=sharing                            |
| Source Code    | This Repository                        |
| Docker Support | Yes                                    |
| AI Models      | Sentence Transformers · FLAN-T5 · NLLB |
# Table of Contents
- About the Project
- Problem Statement & Motivation
- Key Features
- Architecture
- Tech Stack
- Models Used
- Project Structure
- Installation & Setup
- Usage Guide
- Admin Controls
- Screenshots
- Roadmap
- Team
- License
# About the Project
- PolicyNav is an AI-powered platform designed to help users easily understand and navigate complex public policies using advanced Natural Language Processing and machine learning techniques.
- It provides multilingual support, intelligent summarization, semantic search, and knowledge graph visualization to improve accessibility and user understanding.
- Built as part of the Infosys Springboard Internship Final Project.
- Target users include students, citizens, researchers, and policy analysts.
# Problem Statement & Motivation
- Understanding government policies is often difficult due to:
- Complex language and lengthy documents
- Lack of centralized and structured information
- Language barriers for diverse users
- This system uses AI to:
- Simplify policy content
- Provide concise summaries
- Enable multilingual access
- Improve information retrieval through intelligent search
# Key Features
User Features:
| Feature                | Description                                |
| ---------------------- | ------------------------------------------ |
| Secure Authentication  | Login, signup, OTP-based password recovery |
| AI Policy Assistant    | Ask questions and get intelligent answers  |
| Multi-language Support | Query and response translation             |
| Summarization          | Generate concise summaries of policies     |
| Knowledge Graph        | Visualize entities and relationships       |
| Readability Analyzer   | Analyze and simplify text complexity       |
| Global Web Search      | Fetch external policy-related data         |
| Profile Management     | Avatar, email update, password change      |
| Activity History       | Track user interactions                    |
| Feedback System        | Ratings and comments                       |

Admin Features:
- Manage users (view, delete, block)
- Monitor feedback and ratings
- View system activity logs
- Access user statistics dashboard
# Architecture
Monolithic architecture with integrated AI modules and database.
- User → Streamlit UI → Backend (Python) → AI Models → Database
- policy nav architecture
<img width="1536" height="1024" alt="PolicyNav System Architecture   Data Flow" src="https://github.com/user-attachments/assets/85ad2e6b-9e81-4d57-9370-db36b82d4d71" />

# Tech Stack

| Layer         | Technology                |
| ------------- | ------------------------- |
| Frontend      | Streamlit                 |
| Backend       | Python                    |
| Database      | SQLite                    |
| AI Models     | Hugging Face Transformers |
| Search        | FAISS                     |
| NLP           | SpaCy                     |
| Visualization | PyVis                     |
| Security      | JWT, bcrypt, OTP          |
| Deployment    | Docker                    |
# Models Used
| Model                 | Purpose                        | Framework    |
| --------------------- | ------------------------------ | ------------ |
| Sentence Transformers | Semantic search and embeddings | Transformers |
| FLAN-T5               | Summarization                  | Transformers |
| NLLB                  | Language translation           | Transformers |
| SpaCy                 | Entity extraction              | NLP          |
# Installation & Setup
- Prerequisites:
- Python 3.10+
- Git
- Optional: Docker
- Local Setup:
- git clone <repository-link>
- cd PolicyNav
- pip install -r requirements.txt
- Run Application:
- streamlit run app.py
# Usage Guide
- Register or login
- Ask policy-related questions
- View summarized outputs
- Explore knowledge graphs
- Translate content if required
- Analyze readability
- Manage profile and settings
- Provide feedback

# Milestone 1 – Secure User Authentication System

## Project Title
PolicyNav – Public Policy Navigation Using AI  
Milestone 1: Secure User Authentication Module

---

## Description

In this milestone, a secure user authentication system was developed using **Streamlit**, **JWT (JSON Web Token)**, **SQLite**, and **Ngrok**.

This authentication module serves as the foundation for the PolicyNav project and ensures secure user registration, login, session management, and password recovery.

---

## Technologies Used

- Python 3
- Streamlit (Frontend UI)
- SQLite (Database)
- JWT – JSON Web Token (Authentication & Session Management)
- hashlib (Password Hashing using SHA-256)
- Ngrok (Expose local app to public URL)

---

## Features Implemented

### 1. User Signup
- Username (Mandatory)
- Email (Validated format)
- Password (Alphanumeric validation)
- Confirm Password (Must match)
- Security Question (Dropdown)
- Security Answer
- Password stored securely using hashing
- Data stored in SQLite database

---

### 2. Secure Login
- Email verification from database
- Password hash comparison
- JWT token generation upon successful login
- Token expiration (30 minutes session time)

---

### 3. Dashboard
- Welcome message displaying username
- JWT verification before access
- Logout functionality

---

### 4. Forgot Password Flow
1. User enters registered email
2. System verifies email existence
3. Displays stored security question
4. User enters correct security answer
5. Allows password reset
6. Updates password securely in database

---

### 5. JWT Authentication
- Token generated after login
- Token contains:
  - User email
  - Username
  - Expiration time
- Token verified on every dashboard access
- Expired or tampered tokens are rejected

---

### 6. Ngrok Integration
- Application exposed to internet using Ngrok
- Link: https://ngrok.com/
- Public URL generated for demonstration
- Ngrok authtoken removed before GitHub upload (for security)

---

## Database Structure

SQLite database file: `users.db`

Table: `users`

| Column              | Type    |
|---------------------|---------|
| id                  | INTEGER |
| username            | TEXT    |
| email               | TEXT (Unique) |
| password            | TEXT (Hashed) |
| security_question   | TEXT    |
| security_answer     | TEXT (Hashed) |

---

## How to Run the Application (Local Setup)

### Step 1: Install Dependencies

```bash
pip install streamlit pyjwt
streamlit run app.py
ngrok http 8501
```


# PolicyNav - Milestone 2

##  Enhanced Authentication System

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

##  How to Run

1. Open the Colab notebook
2. Add required secrets:
   - `EMAIL_ID` - Your Gmail
   - `EMAIL_APP_PASSWORD` - 16-digit app password
   - `NGROK_AUTHTOKEN` - Your ngrok token
3. Run all cells in order
4. Click the generated URL

##  Files Included
- `app.py` - Main application
- `styles.py` - CSS styling
- `templates.py` - HTML templates
- `readability.py` - Readability analyzer
- Screenshots (png files)

##  Testing Instructions
1. Register a new user
2. Login with credentials
3. Test Forgot Password with OTP
4. Try 3 wrong logins to trigger lock
5. Test Readability with sample text
6. Upload PDF/TXT files


# PolicyNav - Milestone 3: Full AI Integration & Secure Dashboard

## Overview
Milestone 3 represents a massive leap forward for **PolicyNav**. We successfully merged a production-grade, secure authentication backend with a comprehensive suite of AI-powered policy analysis tools. The application now operates as a cohesive, full-stack Streamlit web application with role-based access control, a unified dark/neon UI, and multiple NLP (Natural Language Processing) capabilities to analyze, summarize, and translate Indian Government policies.

---

## Key Features & Modules Added

### 1. Secure Authentication & Admin Routing
We integrated a robust security backend to protect the AI tools. Features include:
* **JWT Authentication:** Secure login sessions using JSON Web Tokens.
* **Password Security:** `bcrypt` hashing, password strength validation, and prevention of reusing old passwords.
* **Rate Limiting & Lockouts:** Prevents brute-force attacks by locking accounts after 3 failed attempts.
* **OTP Email Recovery:** Integrated SMTP email routing to send 6-digit one-time passwords for secure account recovery.
* **Admin Control Panel:** A dedicated dashboard for administrators to view, manage, and delete user accounts.


### 2. Multilingual RAG Q&A Engine (AI Policy Assistant)
A Retrieval-Augmented Generation (RAG) system built to answer questions accurately based strictly on official policy documents.
* **Vector Database:** Uses `FAISS` and `SentenceTransformers` (`all-MiniLM-L6-v2`) to search through chunks of policy PDFs.
* **Generative AI:** Uses Hugging Face's `google/flan-t5-base` to read the retrieved context and generate a conversational answer.
* **Multilingual Support:** Automatically translates the user's question to English for searching, and translates the AI's final answer back to the user's preferred regional language (Hindi, Telugu, Tamil, etc.).


### 3. AI Policy Summarization
Condenses long, complex government texts into digestible bullet points.
* **Prompt Engineering:** We utilize strict prompt parameters (`max_new_tokens`, `min_length`, `num_beams`) on the `FLAN-T5` model to force detailed, multi-sentence paragraph generation rather than single-line outputs.
* **Instant Translation:** Outputs can be seamlessly translated into 10 different Indian languages.


### 4. Entity Knowledge Graph (Web)
Visualizes how government policies interact with different organizations, locations, and dates.
* **NLP Extraction:** Uses `spaCy` (`en_core_web_sm`) to perform Named Entity Recognition (NER) on policy text.
* **Interactive UI:** Built using `NetworkX` and `Pyvis`, allowing users to drag, drop, and zoom into nodes (documents) and edges (extracted entities like ministries or states) directly in the browser.


### 5. Text Readability Analyzer
A dashboard designed to evaluate the complexity of government documents to ensure they are accessible to the public.
* **Metrics:** Calculates Flesch Reading Ease, Flesch-Kincaid Grade, SMOG Index, Gunning Fog, and Coleman-Liau metrics using `textstat`.
* **UI/UX:** Features interactive gauge charts via `Plotly` and statistical text breakdowns (syllables, complex words, sentence count). Supports both direct text pasting and PDF uploads via `PyPDF2`.


### 6. Live Web Research
A supplementary tool that fetches real-time information from the web to complement our static PDF vector database.
* **Implementation:** Utilizes the `wikipedia` API wrapper to safely and reliably fetch summaries and source links for government officials, new schemes, or political entities without getting blocked by bot-protections in cloud environments.


### 7. Standalone Text Translator
A fast, dedicated utility for users to paste raw policy text and instantly translate it between English and supported Indian regional languages using `deep-translator`.


## 8. Interactive Feedback & Administration

A direct communication channel between users and administrators that supports continuous platform improvement and enhances accessibility to policy-related resources.

### User Feedback Portal
- Provides a **professional 5-star rating slider** along with a **detailed text input field** for qualitative feedback.
- Implements **strict validation rules** to prevent empty or meaningless submissions.
- Ensures that all feedback entries contain meaningful user input before processing.

### Admin Visibility
- All feedback submissions are securely stored in a **dedicated SQLite database table**.
- The stored feedback is accessible **only through the Administrator Control Panel**.
- Administrators can review user feedback to identify improvements and address issues on the platform.

### Input Integrity
- Backend validation mechanisms ensure that feedback is **only saved when valid content is provided**.
- Prevents blank ratings or empty text submissions from being stored in the system.


---

## 9. Personal Activity History

A persistence-driven monitoring feature that allows users to track and revisit their previous interactions with the platform.

### Comprehensive Persistence
- Records the **user prompt**, **AI-generated response**, and the **specific tool used** during the interaction.
- Ensures that important information and insights remain accessible for future reference.

### Expander-Based User Interface
- Displays interaction history in a **clean chronological format**.
- Uses **expandable sections** that allow users to open individual entries and view full prompt–response details without cluttering the main interface.

  
---

## Technology Stack
* **Frontend UI:** Streamlit, Streamlit-Option-Menu, Plotly, HTML/CSS injected styling.
* **Backend Database:** SQLite (User DB & Policy Metadata DB).
* **Security:** PyJWT, bcrypt, hmac, hashlib, smtplib.
* **AI & Machine Learning:** HuggingFace Transformers (`google/flan-t5-base`), Sentence-Transformers (`all-MiniLM-L6-v2`), FAISS (Facebook AI Similarity Search), spaCy.
* **Data Processing:** PyPDF2, textstat, NetworkX, Pyvis, BeautifulSoup4.

---

## How to Run the Application (Google Colab)
Since the FAISS vector database and parsed chunks are already saved in Google Drive, there is no need to re-download or re-process the PDFs. 

1. **Mount Google Drive** to access the pre-processed database: `policy_vector_db.index` and `chunks.pkl`.
2. **Install Dependencies:**
   ```bash
   pip install streamlit pyjwt bcrypt python-dotenv pyngrok nltk streamlit-option-menu plotly textstat PyPDF2 transformers deep-translator pyvis sentence-transformers faiss-cpu wikipedia spacy
   python -m spacy download en_core_web_sm


# PolicyNav - Milestone 4: End-to-End Application & Admin Analytics

## Overview
Milestone 4 represents the final integration phase of the Infosys Springboard Internship. This phase elevates the project from a suite of AI tools into a fully managed, enterprise-grade SaaS platform. It introduces a comprehensive **Admin Command Center** for real-time data analytics and a **User Profile** portal for identity and strict security management.

---

## 1. Admin Dashboard (Management & Analytics)
The Admin panel has been engineered as a central command center, equipping administrators with powerful oversight, database management, and reporting capabilities.

### User Control
The system implements strict Role-Based Access Control (RBAC). Administrators can instantly elevate standard accounts to Admin status, granting them full dashboard access. To maintain platform integrity, Admins can manually lock or unlock accounts to mitigate compromised credentials. Furthermore, Admins can permanently delete users, which safely cascades the deletion across all relational database tables (clearing their history, OTPs, and feedback).


### Activity Tracking
A comprehensive auditing module allows Admins to view an aggregated, chronological feed of all user interactions. This tracks exact AI prompts, generated responses, tool usage, and timestamps across the entire platform, providing a transparent view of real-time system engagement and user behavior.


### Data Visualization
Leveraging `pandas` for data manipulation and `plotly.express` for dynamic rendering, the dashboard generates interactive, dark-themed visualizations to provide actionable business intelligence. 
* **Model & Feature Popularity:** Bar charts dynamically track and display which AI tools (e.g., AI Policy Assistant vs. Summarizer) are driving the most user engagement.
* **Language Utilization:** Interactive pie charts map the distribution of regional language outputs, highlighting the platform's linguistic reach and accessibility impact across different demographics.


### Feedback Analysis
To process qualitative data efficiently, the platform automatically aggregates all text-based user comments from the feedback databases. It utilizes the `wordcloud` and `matplotlib` libraries to render a visual sentiment map. This allows administrators to instantly identify recurring themes, highly requested features, and common pain points at a single glance without reading hundreds of individual rows.

### Data Export
For offline analysis and compliance reporting, the system features instant 1-click data extraction. Using Pandas dataframe conversions, administrators can download comprehensive `.csv` files containing the complete user directory, full activity logs, and granular AI tool performance feedback directly to their local machines.

---

## 2. User Dashboard & Profile Personalization
The standard user experience has been highly personalized and secured, giving users complete autonomy over their accounts and data.

### Security Settings
Users are empowered to manage their own credentials through a highly secure interface. 
* **Email Updates:** Updating an email address safely cascades the change across all relational database tables (history, feedback, etc.) so no user data is orphaned or lost.
* **Password Management:** Password changes require strict verification of the current password and check the database history to prevent the reuse of recent passwords. Upon a successful password change, the system automatically triggers a forced cache clear and session logout, kicking the user to the login screen to ensure maximum account security.


### Identity & Avatar (DP) Personalization
To personalize the SaaS experience, users can upload a custom Profile Avatar (PNG/JPG). 
* **Smart Storage:** Instead of relying on complex external cloud storage buckets, the uploaded image is converted directly into a Base64 encoded string and stored natively within the SQLite database.
* **Validation & UI:** The system includes a strict 5MB backend file size validation check. Upon a successful upload, the Base64 string instantly decodes and updates the application's sidebar UI, replacing the default placeholder icon with the user's custom image. 


## Technology Stack
* **Frontend UI & Personalization:** Streamlit, Streamlit Components, Custom HTML/CSS injected styling (Animations, Native SVG injection).
* **Data Science & Analytics:** Pandas (Dataframe manipulation), Plotly Express (Interactive charts), Matplotlib, WordCloud (Sentiment visualization).
* **Backend Database:** SQLite (Relational User DB, Roles, Base64 Image Storage, & Policy Metadata DB).
* **Security & Authentication:** PyJWT, bcrypt, hmac, hashlib, smtplib (SMTP Routing), Base64 (Secure avatar encoding).
* **AI & Machine Learning:** HuggingFace Transformers (`google/flan-t5-base`), Sentence-Transformers (`all-MiniLM-L6-v2`), FAISS (Facebook AI Similarity Search), spaCy.
* **Data Processing & Scraping:** PyPDF2, textstat, NetworkX, Pyvis, Wikipedia API.

---

## How to Run the Application (Google Colab)
Since the FAISS vector database, parsed chunks, and the comprehensive SQLite user database are permanently saved in Google Drive, there is no need to re-download or re-process the PDFs. 

1. **Mount Google Drive** to access the pre-processed backend files: `policy_vector_db.index`, `chunks.pkl`, and `users.db`.
2. **Install Dependencies:** (Note: This now includes the heavy Data Science libraries required for the Admin Analytics Dashboard).
   ```bash
   pip install streamlit pyjwt bcrypt python-dotenv pyngrok nltk plotly textstat PyPDF2 transformers deep-translator pyvis sentence-transformers faiss-cpu wikipedia spacy pandas matplotlib wordcloud
   python -m spacy download en_core_web_sm


# Screenshots
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 34 04 PM" src="https://github.com/user-attachments/assets/e35391b4-41ce-4006-b521-cd6651f306c3" />

<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 35 44 PM" src="https://github.com/user-attachments/assets/c51c7169-7e4f-4f64-ae44-cd36a6f5651b" />

<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 36 03 PM" src="https://github.com/user-attachments/assets/daab2ea0-100e-42c6-96a7-5ff13f8732b5" />

<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 01 PM" src="https://github.com/user-attachments/assets/50d06552-7da2-4185-8a2f-31920e09241b" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 44 PM" src="https://github.com/user-attachments/assets/72da7491-3595-4c43-84dc-1810dd279d7a" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 28 01 PM" src="https://github.com/user-attachments/assets/15a2676d-0df6-4516-9eed-20a59b886e4b" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 54 PM" src="https://github.com/user-attachments/assets/c11de090-993b-4368-9508-f906293858eb" />
<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 08 36 PM" src="https://github.com/user-attachments/assets/77b87fee-d069-4d7f-b471-dd7520684e7b" />
<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 08 46 PM" src="https://github.com/user-attachments/assets/fb1defe8-d274-4911-a9e4-2ea5bc3884bc" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 00 PM" src="https://github.com/user-attachments/assets/d96afe62-d249-437f-83cf-047d2a6371fc" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 11 PM" src="https://github.com/user-attachments/assets/10241c6c-97e9-4755-81da-480955061560" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 09 29 PM" src="https://github.com/user-attachments/assets/73d123bc-b583-49bc-b486-0088db210c96" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 26 22 PM" src="https://github.com/user-attachments/assets/f2cfc07c-a6cd-44de-8602-0bf68c9683b1" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 37 PM" src="https://github.com/user-attachments/assets/b9076530-ee43-4ebb-9119-39b371e6d260" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 50 PM" src="https://github.com/user-attachments/assets/27704673-9d08-4de6-9834-2bed4f415bcb" />

<img width="1440" height="900" alt="Screenshot 2026-03-12 at 5 07 23 PM" src="https://github.com/user-attachments/assets/ab80b983-8fc6-4447-a8aa-ea23daed5369" />


# Roadmap
- Improve model performance
- Add more datasets
- Enhance UI/UX
- Deploy on cloud platform
- Add voice-based interaction
# Team
| Name                          | Role                              |
| ----------------------------- | --------------------------------- |
| Shambhavi Jha                 | AI and NLP Development            |
| Srideepalakshmi Muruganantham | Backend and Security              |
| Mainuddeen                    | Summarization and Web Integration |
| Bhuvaneshwar Reddy Mandadapu  | Profile and System Integration    |
| Arjun L Nair                  | Testing and Deployment            |
# License
MIT License
- Free to use, modify, and distribute with proper credits.
