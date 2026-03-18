# Infosys Springboard
# 🧠 PolicyNav - Public-Policy-Navigation-Using-AI
AI-Powered Public Policy Navigation and Intelligence Platform
Simplifying complex government policies through multilingual AI, summarization, and intelligent search.
# 🔗 Links: 
| Category       | Link                                   |
| -------------- | -------------------------------------- |
| Demo Video     | Coming Soon                            |
| Source Code    | This Repository                        |
| Docker Support | Yes                                    |
| AI Models      | Sentence Transformers · FLAN-T5 · NLLB |
# 📌 Table of Contents
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
# 📖 About the Project
- PolicyNav is an AI-powered platform designed to help users easily understand and navigate complex public policies using advanced Natural Language Processing and machine learning techniques.
- It provides multilingual support, intelligent summarization, semantic search, and knowledge graph visualization to improve accessibility and user understanding.
- Built as part of the Infosys Springboard Internship Final Project.
- Target users include students, citizens, researchers, and policy analysts.
# 🎯 Problem Statement & Motivation
- Understanding government policies is often difficult due to:
- Complex language and lengthy documents
- Lack of centralized and structured information
- Language barriers for diverse users
- This system uses AI to:
- Simplify policy content
- Provide concise summaries
- Enable multilingual access
- Improve information retrieval through intelligent search
# 🚀 Key Features
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
# 🧩 Architecture
Monolithic architecture with integrated AI modules and database.
- User → Streamlit UI → Backend (Python) → AI Models → Database
![policy nav architecture](https://github.com/user-attachments/assets/ffe8fe9a-ee6e-4577-bb3f-fc763a65530c)
# 🛠 Tech Stack
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
# 🤖 Models Used
| Model                 | Purpose                        | Framework    |
| --------------------- | ------------------------------ | ------------ |
| Sentence Transformers | Semantic search and embeddings | Transformers |
| FLAN-T5               | Summarization                  | Transformers |
| NLLB                  | Language translation           | Transformers |
| SpaCy                 | Entity extraction              | NLP          |
# ⚙️ Installation & Setup
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
# 📝 Usage Guide
- Register or login
- Ask policy-related questions
- View summarized outputs
- Explore knowledge graphs
- Translate content if required
- Analyze readability
- Manage profile and settings
- Provide feedback
# 📸 Screenshots
# 📊 Roadmap
- Improve model performance
- Add more datasets
- Enhance UI/UX
- Deploy on cloud platform
- Add voice-based interaction
# 👥 Team
| Name                          | Role                              |
| ----------------------------- | --------------------------------- |
| Shambhavi Jha                 | AI and NLP Development            |
| Srideepalakshmi Muruganantham | Backend and Security              |
| Mainuddeen                    | Summarization and Web Integration |
| Bhuvaneshwar Reddy Mandadapu  | Profile and System Integration    |
| Arjun L Nair                  | Testing and Deployment            |
# 📜 License
MIT License
- Free to use, modify, and distribute with proper credits.
