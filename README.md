# CodeMedic AI

Live Demo: https://codemedic-repo.vercel.app/

CodeMedic AI is an AI-powered code review assistant that analyzes GitHub repositories, detects potential issues, explains code, suggests improvements, generates documentation, and helps developers improve software quality using AI agents.

---

## Overview

CodeMedic AI automates the code review process by analyzing a developer's GitHub repository and providing intelligent feedback.

Developers can connect their repository and receive AI-generated insights about bugs, code quality, security concerns, documentation, and testing opportunities.

---

## Features

### Repository Analysis
- Analyze public GitHub repositories
- Understand project structure and code organization
- Review files automatically using AI

### Bug Detection
- Detect potential bugs and logical issues
- Explain the cause of problems
- Suggest possible fixes

### Code Improvements
- Identify inefficient code
- Suggest better coding practices
- Improve readability and maintainability

### Documentation Generation
- Generate documentation automatically
- Explain complex code sections

### Unit Test Generation
- Generate test cases
- Improve code reliability

### Security Review
- Identify possible security issues
- Suggest safer implementations

### AI Agent Workflow
AI agents work together to:
- Analyze repositories
- Review code quality
- Generate recommendations
- Provide actionable feedback

---

## Architecture

```
User
 |
React Frontend
 |
FastAPI Backend
 |
AI Processing Layer
 |
GitHub Repository
```

---

## Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Axios

### Backend
- FastAPI
- Python
- OpenAI API
- GitHub API

### Deployment
- Vercel (Frontend)
- Render (Backend)

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/yourusername/codemedic-ai.git

cd codemedic-ai
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

Activate environment:

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token
CORS_ORIGINS=http://localhost:5173
```

Run backend:

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Project Structure

```
CodeMedic-AI
|
├── frontend
│   ├── src
│   ├── public
│   └── package.json
|
├── backend
│   ├── routers
│   ├── services
│   ├── main.py
│   └── requirements.txt
|
└── README.md
```

---

## Future Improvements

- GitHub OAuth integration
- Private repository support
- Automatic pull request reviews
- AI-generated commits
- CI/CD integration
- More specialized AI coding agents

---

## Developer

Mithesh Makam

Built for an Agentic Coding Hackathon.
