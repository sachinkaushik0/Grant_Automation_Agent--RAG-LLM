# FindGrant: LLM-Powered Grant Automation

**AI-powered platform for automating grant eligibility assessment and proposal drafting.**

---

## Overview

**FindGrant** is a production-ready **LLM-driven grant automation system** developed during my internship at **DistApps Inc.** It leverages **Google Gemini 1.5 Flash** and locally hosted **Ollama LLMs** to dynamically assess eligibility and draft proposals. Using a **Retrieval-Augmented Generation (RAG) architecture**, the platform combines **FAISS/ChromaDB semantic search** with modular prompt templates for precise, context-aware completions.

A scalable **FastAPI backend** with AWS serverless integrations handles user intake, document storage, and LLM output, enabling a seamless and automated grant application workflow.

---

## Key Features

- **LLM Integration:** Prompt-engineered **Gemini 1.5 Flash** and **Ollama LLMs** for dynamic proposal generation and eligibility assessment.  
- **RAG Architecture:** Combines **FAISS** or **ChromaDB** semantic search with modular prompts for accurate, context-aware completions.  
- **Backend API:** **FastAPI** endpoints for user intake, grant matching, and LLM responses.  
- **Cloud & Serverless:** AWS S3 for secure document storage, AWS Lambda for event-driven automation.  
- **Performance & Scalability:** Optimized LLMs and architecture to handle high-volume requests with minimal latency.  
- **Impact:** Improved grant application turnaround by **70%**, validated via functional tests and stakeholder feedback.  

---

## Architecture

```text
       +--------------------+
       | User Grant Request |
       +---------+----------+
                 |
                 v
        +------------------+
        | FastAPI Backend  |
        +------------------+
        | Intake & Routing |
                 |
                 v
      +-------------------------+
      | RAG + LLM Processing    |
      | FAISS / ChromaDB        |
      | Gemini 1.5 / Ollama LLM|
      +-------------------------+
                 |
                 v
      +-------------------------+
      | Proposal Output & Docs  |
      +-------------------------+
                 |
                 v
         AWS S3 Storage & Lambda
---
# Tech Stack
Language: Python

LLM: Google Gemini 1.5 Flash, Ollama

RAG / Search: FAISS, ChromaDB

Backend / API: FastAPI

Cloud / Serverless: AWS S3, AWS Lambda

Other: Prompt Engineering, Modular Templates

Getting Started
Prerequisites
Python 3.10+

Access to LLM models (Gemini 1.5 Flash, Ollama)

AWS account with S3 and Lambda configured

Installation
bash
Copy
Edit
# Clone the repository
git clone https://github.com/sachinkaushik0/Grant_Automation_Agent.git
cd Grant_Automation_Agent

# Install dependencies
pip install -r requirements.txt

# Run backend locally
uvicorn back_end.main:app --reload
Usage
Submit grant documents or eligibility queries through the API.

The RAG + LLM pipeline processes the input, retrieving relevant context and generating a proposal.

Outputs are stored securely in AWS S3 and accessible via API or dashboard.

Results
70% faster grant application turnaround compared to manual processing.

Production-ready pipeline capable of handling real-time requests.

Fully automated, cloud-integrated workflow for grant management.

Contact
Sachin Kaushik

GitHub: sachinkaushik0

Email: sachinkaushikca@gmail.com
