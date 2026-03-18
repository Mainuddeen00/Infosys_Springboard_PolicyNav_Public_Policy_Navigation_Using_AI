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
![policy nav architecture](https://github.com/user-attachments/assets/ffe8fe9a-ee6e-4577-bb3f-fc763a65530c)
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
