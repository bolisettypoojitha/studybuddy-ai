# 🧠 StudyBuddy

**StudyBuddy** is your intelligent and interactive learning companion built using **Python, Flask, PostgreSQL**, and **Large Language Models (LLMs)** like Gemini and Hugging Face. It helps students take smart notes, generate flashcards, create quizzes, plan studies, and stay productive.

---


## 🌟 Features

### 🔐 Authentication
- Secure registration and login with hashed passwords
- CSRF protection and session management
- "Remember me" login support

### 📝 Notes Management
- Add, edit, delete notes with subject & topic
- Search notes by keyword
- Summarize notes using Gemini or Hugging Face

### 🧠 Flashcards & Quizzes (Gemini API)
- Generate flashcards from notes using LLM
- Auto-generate multiple-choice questions for revision
- Interactive flip-style flashcard UI

### 📅 Study Planner
- Assign study topics to specific dates
- View and manage weekly plans with Chart.js graphs

### ✅ To-Do List
- Add personal study tasks
- Mark tasks as complete/incomplete
- Delete or update status of tasks

### ⏱️ Study Timer
- Built-in Pomodoro timer (Start, Pause, Reset)
- Visual alerts and focus-friendly UI

---

## ⚙️ Tech Stack

| Layer            | Tools/Libraries                                      |
|------------------|------------------------------------------------------|
| **Frontend**     | HTML5, CSS3, JavaScript, Bootstrap 5, AOS Animations |
| **Backend**      | Flask, Flask-Login, Flask-WTF, Flask-Migrate         |
| **Database**     | PostgreSQL, SQLAlchemy ORM                           |
| **AI/LLM**       | Gemini API (Google) + Hugging Face Transformers API  |
| **Styling**      | Dark Mode toggle, custom themes, responsive layout   |

---

## 🗂️ Folder Structure

StudyBuddy/
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes/ # auth.py, notes.py, planner.py, etc.
│ ├── templates/ # HTML templates
│ ├── static/ # CSS, JS, dark mode, animations
│ └── utilities/ # gemini_utils.py, huggingface_utils.py
│
├── migrations/ # Flask-Migrate versions
├── .env # API keys and DB URL
├── config.py # Configuration settings
├── requirements.txt
├── run.py
└── README.md 
