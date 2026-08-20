# 🚀 AI-Powered Resume-Job Matcher

An AI-driven Applicant Tracking System (ATS) optimizer that analyzes a candidate's resume against a specific job description. It calculates a match score, identifies missing skills, and uses a Large Language Model (LLM) to provide highly actionable, custom-tailored feedback to help candidates land the interview.

## ✨ Features
* **Resume Parsing:** Upload a PDF resume, and the backend automatically extracts and processes the text.
* **Smart Skill Matching:** Compares the job description requirements against the resume to generate a customized ATS compatibility score.
* **Gap Analysis:** Specifically identifies which required technologies or skills are missing from the candidate's resume.
* **AI Career Coach:** Integrates with Groq (Llama 3.1) to generate two distinct feedback sections:
  1. **Skills to Learn:** What the candidate needs to study to become a stronger fit.
  2. **How to Rewrite:** Exact bullet points and phrasing the candidate can copy/paste to optimize their resume for ATS scanners.
* **Clean UI:** Built with React, featuring Markdown-rendered AI feedback for high readability.

## 🛠️ Tech Stack
* **Frontend:** React.js, Vite, React-Markdown
* **Backend:** Python, FastAPI, Uvicorn
* **AI Integration:** Groq API (llama-3.1-8b-instant)

## 💻 Running the App Locally

### Prerequisites
Make sure you have [Node.js](https://nodejs.org/) and [Python](https://www.python.org/) installed on your machine. You will also need a free API key from [Groq](https://console.groq.com/).

### 1. Setup the Backend (PowerShell)
Open a terminal and navigate to the `backend` folder:
```powershell
cd backend