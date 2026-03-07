
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

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 28 17 PM" src="https://github.com/user-attachments/assets/98fdaf45-be89-4b58-97e5-3ee9d92b4947" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 50 09 PM" src="https://github.com/user-attachments/assets/aa6e3130-d3f1-4012-a412-bccb298c410e" />







### 2. Multilingual RAG Q&A Engine (AI Policy Assistant)
A Retrieval-Augmented Generation (RAG) system built to answer questions accurately based strictly on official policy documents.
* **Vector Database:** Uses `FAISS` and `SentenceTransformers` (`all-MiniLM-L6-v2`) to search through chunks of policy PDFs.
* **Generative AI:** Uses Hugging Face's `google/flan-t5-base` to read the retrieved context and generate a conversational answer.
* **Multilingual Support:** Automatically translates the user's question to English for searching, and translates the AI's final answer back to the user's preferred regional language (Hindi, Telugu, Tamil, etc.).

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 34 04 PM" src="https://github.com/user-attachments/assets/e35391b4-41ce-4006-b521-cd6651f306c3" />






### 3. AI Policy Summarization
Condenses long, complex government texts into digestible bullet points.
* **Prompt Engineering:** We utilize strict prompt parameters (`max_new_tokens`, `min_length`, `num_beams`) on the `FLAN-T5` model to force detailed, multi-sentence paragraph generation rather than single-line outputs.
* **Instant Translation:** Outputs can be seamlessly translated into 10 different Indian languages.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 35 28 PM" src="https://github.com/user-attachments/assets/0c8aeabb-d4f9-4e3d-b06a-8f804e15834d" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 34 51 PM" src="https://github.com/user-attachments/assets/e55e00f5-ae86-4f3a-a940-f0d6955e29b9" />





### 4. Entity Knowledge Graph (Web)
Visualizes how government policies interact with different organizations, locations, and dates.
* **NLP Extraction:** Uses `spaCy` (`en_core_web_sm`) to perform Named Entity Recognition (NER) on policy text.
* **Interactive UI:** Built using `NetworkX` and `Pyvis`, allowing users to drag, drop, and zoom into nodes (documents) and edges (extracted entities like ministries or states) directly in the browser.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 35 44 PM" src="https://github.com/user-attachments/assets/c51c7169-7e4f-4f64-ae44-cd36a6f5651b" />



### 5. Text Readability Analyzer
A dashboard designed to evaluate the complexity of government documents to ensure they are accessible to the public.
* **Metrics:** Calculates Flesch Reading Ease, Flesch-Kincaid Grade, SMOG Index, Gunning Fog, and Coleman-Liau metrics using `textstat`.
* **UI/UX:** Features interactive gauge charts via `Plotly` and statistical text breakdowns (syllables, complex words, sentence count). Supports both direct text pasting and PDF uploads via `PyPDF2`.


### 6. Live Web Research
A supplementary tool that fetches real-time information from the web to complement our static PDF vector database.
* **Implementation:** Utilizes the `wikipedia` API wrapper to safely and reliably fetch summaries and source links for government officials, new schemes, or political entities without getting blocked by bot-protections in cloud environments.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 36 03 PM" src="https://github.com/user-attachments/assets/daab2ea0-100e-42c6-96a7-5ff13f8732b5" />



### 7. Standalone Text Translator
A fast, dedicated utility for users to paste raw policy text and instantly translate it between English and supported Indian regional languages using `deep-translator`.

<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 01 PM" src="https://github.com/user-attachments/assets/50d06552-7da2-4185-8a2f-31920e09241b" />
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 44 PM" src="https://github.com/user-attachments/assets/72da7491-3595-4c43-84dc-1810dd279d7a" />



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

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 28 01 PM" src="https://github.com/user-attachments/assets/15a2676d-0df6-4516-9eed-20a59b886e4b" />


---

## 9. Personal Activity History

A persistence-driven monitoring feature that allows users to track and revisit their previous interactions with the platform.

### Comprehensive Persistence
- Records the **user prompt**, **AI-generated response**, and the **specific tool used** during the interaction.
- Ensures that important information and insights remain accessible for future reference.

### Expander-Based User Interface
- Displays interaction history in a **clean chronological format**.
- Uses **expandable sections** that allow users to open individual entries and view full prompt–response details without cluttering the main interface.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-07 at 2 38 54 PM" src="https://github.com/user-attachments/assets/c11de090-993b-4368-9508-f906293858eb" />


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
