# 🚀 AI README Generator

A modern AI-powered web application that automatically generates professional `README.md` files from uploaded project ZIP files.

Built using **Python**, **Dash**, and **Groq (Llama 3.3 70B)**, the application analyzes your project structure, understands your source code, and produces clean, developer-friendly documentation within seconds.

---

### ✨ Why use it?

Writing documentation is repetitive and time-consuming.

This application lets developers simply upload a project ZIP file and instantly receive a structured README complete with installation steps, project overview, features, folder structure, usage instructions, and more.

![Python](https://img.shields.io/badge/Python-3.10+-blue)

![Dash](https://img.shields.io/badge/Dash-Framework-green)

![Groq](https://img.shields.io/badge/LLM-Groq-orange)

![License](https://img.shields.io/badge/License-MIT-yellow)

![Status](https://img.shields.io/badge/Status-Active-success)

## ✨ Features

- 📦 Upload project ZIP files with drag-and-drop support
- 🤖 AI-powered README generation using Groq (Llama 3.3 70B)
- 📂 Automatic project structure analysis
- 📝 Editable Markdown editor
- 👀 Real-time Markdown preview
- 📥 Download README.md instantly
- 🌗 Light & Dark mode support
- ⚡ Fast generation with secure temporary file handling

## ⚙️ Workflow

```text
Upload ZIP
      │
      ▼
Extract Project Files
      │
      ▼
Analyze Project Structure
      │
      ▼
Generate AI Prompt
      │
      ▼
Groq Llama 3.3 70B
      │
      ▼
Generate README
      │
      ▼
Edit & Preview
      │
      ▼
Download README.md
```

## 🛠 Tech Stack

### Frontend

- Dash
- Dash Bootstrap Components
- HTML
- CSS

### Backend

- Python
- Dash Callbacks

### AI

- Groq API
- Llama 3.3 70B

### Utilities

- Python Dotenv
- Markdown
- ZIP Processing

## 🏗 System Architecture

```text
Browser
     │
     ▼
Dash Application
     │
     ├── ZIP Upload
     ├── Project Parser
     ├── Prompt Builder
     ├── Groq AI
     ├── Markdown Editor
     └── Live Preview
```
# 📁 Project Structure

```
ai-readme-generator/
├── app.py                 # Main Dash application
├── assets/
│   └── styles.css        # Custom CSS styles (with Dark Mode support)
├── callbacks/
│   ├── upload_callbacks.py    # File upload handling
│   ├── ai_callbacks.py        # AI generation callbacks
│   └── editor_callbacks.py   # Editor, theme toggle, and preview callbacks
├── services/
│   ├── zip_service.py        # ZIP extraction and handling
│   ├── parser_service.py     # Project file parsing
│   ├── prompt_service.py     # AI prompt building
│   └── gemini_service.py     # Groq API integration (handles API calls)
├── utils/
│   └── markdown_utils.py     # Markdown processing utilities
├── temp_uploads/            # Temporary upload storage
├── .env.example            # Template for environment variables
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://127.0.0.1:8050/'


3. Upload your project ZIP file, click **Generate README**, customize it in the editor, and click **Download README**!

## Requirements

- Python 3.8+
- Groq API Key (get one free at [console.groq.com](https://console.groq.com))

## Dependencies

- Dash: Web framework
- dash-bootstrap-components: Bootstrap components for Dash
- groq: Groq Cloud API SDK
- python-dotenv: Environment variable management
- markdown: Markdown parsing and rendering

## 🚀 Future Improvements

- GitHub OAuth Integration
- Direct README Commit to GitHub
- Multiple README Templates
- Mermaid Diagram Generation
- Multi-LLM Support
- Documentation Quality Score
- AI Chat for Project Analysis

## 🔒 Privacy

Uploaded ZIP files are processed temporarily for README generation and are not stored permanently. Temporary files are cleaned up after processing.

## 🌐 Live Demo

(https://readme-ai-generator-la9s.onrender.com/)

## 👩‍💻 Author

**Nivasri T**

Third-Year B.Tech Artificial Intelligence & Data Science Student

GitHub:
https://github.com/NivasriT

LinkedIn:
https://www.linkedin.com/in/nivasri-thirumeni-a6713732a/

