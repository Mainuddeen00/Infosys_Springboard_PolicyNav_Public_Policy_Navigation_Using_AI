
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
<img width="1440" height="900" alt="553597146-6583fdbd-fbbf-4f85-9683-9ba5c6eddbde" src="https://github.com/user-attachments/assets/a7d0b432-bb1e-4f87-b367-b7d2abf8ae9e" />

<img width="1440" height="900" alt="Screenshot 2026-03-06 at 7 54 15 PM" src="https://github.com/user-attachments/assets/a56eb14a-0f3a-4e9d-ad07-4ba07875471e" />




### 2. Multilingual RAG Q&A Engine (Chat)
A Retrieval-Augmented Generation (RAG) system built to answer questions accurately based strictly on official policy documents.
* **Vector Database:** Uses `FAISS` and `SentenceTransformers` (`all-MiniLM-L6-v2`) to search through chunks of policy PDFs.
* **Generative AI:** Uses Hugging Face's `google/flan-t5-base` to read the retrieved context and generate a conversational answer.
* **Multilingual Support:** Automatically translates the user's question to English for searching, and translates the AI's final answer back to the user's preferred regional language (Hindi, Telugu, Tamil, etc.).

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 09 44 PM" src="https://github.com/user-attachments/assets/6fd011aa-0dfd-4eef-bc6e-dfa94241d53a" />

<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 11 49 PM" src="https://github.com/user-attachments/assets/a9f08edd-9dcc-46bc-b109-a1945141f5da" />





### 3. AI Policy Summarization
Condenses long, complex government texts into digestible bullet points.
* **Prompt Engineering:** We utilize strict prompt parameters (`max_new_tokens`, `min_length`, `num_beams`) on the `FLAN-T5` model to force detailed, multi-sentence paragraph generation rather than single-line outputs.
* **Instant Translation:** Outputs can be seamlessly translated into 10 different Indian languages.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 7 59 46 PM" src="https://github.com/user-attachments/assets/c1f656c6-8f70-4934-baa2-55359c45d143" />
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 00 16 PM" src="https://github.com/user-attachments/assets/2dc2c8d1-92e4-4c69-9868-eab3ea822630" />



### 4. Entity Knowledge Graph (Web)
Visualizes how government policies interact with different organizations, locations, and dates.
* **NLP Extraction:** Uses `spaCy` (`en_core_web_sm`) to perform Named Entity Recognition (NER) on policy text.
* **Interactive UI:** Built using `NetworkX` and `Pyvis`, allowing users to drag, drop, and zoom into nodes (documents) and edges (extracted entities like ministries or states) directly in the browser.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 00 43 PM" src="https://github.com/user-attachments/assets/2505a367-979a-42f0-a086-1d4c0671be70" />


### 5. Text Readability Analyzer
A dashboard designed to evaluate the complexity of government documents to ensure they are accessible to the public.
* **Metrics:** Calculates Flesch Reading Ease, Flesch-Kincaid Grade, SMOG Index, Gunning Fog, and Coleman-Liau metrics using `textstat`.
* **UI/UX:** Features interactive gauge charts via `Plotly` and statistical text breakdowns (syllables, complex words, sentence count). Supports both direct text pasting and PDF uploads via `PyPDF2`.

> **Screenshot:**
> *Add your Readability Analyzer screenshot here*
> `![Readability](link_to_your_image.png)`

### 6. Live Web Research
A supplementary tool that fetches real-time information from the web to complement our static PDF vector database.
* **Implementation:** Utilizes the `wikipedia` API wrapper to safely and reliably fetch summaries and source links for government officials, new schemes, or political entities without getting blocked by bot-protections in cloud environments.

> **Screenshot:**
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 01 10 PM" src="https://github.com/user-attachments/assets/d45c1473-62f6-4a33-a3d8-f5a8dd6261b6" />


### 7. Standalone Text Translator
A fast, dedicated utility for users to paste raw policy text and instantly translate it between English and supported Indian regional languages using `deep-translator`.
<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 03 04 PM" src="https://github.com/user-attachments/assets/dfbd2c07-610a-4d55-bfb3-6db5ede96ed3" />

<img width="1440" height="900" alt="Screenshot 2026-03-06 at 8 22 47 PM" src="https://github.com/user-attachments/assets/296f01df-5489-487f-b0dd-196e8fd284e3" />




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
