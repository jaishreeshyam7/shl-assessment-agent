# SHL Assessment Recommendation Agent

This project was developed as part of the SHL AI Intern assignment.

The goal of this project is to build a conversational recommendation system that helps recruiters find the most suitable SHL assessments based on a hiring requirement. Instead of returning simple keyword matches, the system understands the user's intent, asks follow-up questions when necessary, performs semantic search over the SHL catalog using FAISS, and generates concise explanations using Google's Gemini model.

---

## Live Demo

**API Documentation (Swagger)**

https://shl-assessment-agent-production-ac55.up.railway.app/docs#/default/chat_chat_post

**GitHub Repository**

:contentReference[oaicite:0]{index=0}

---

# Features

- Conversational recommendation system
- Multi-turn conversation support
- Automatic clarification questions
- Semantic search using FAISS
- Gemini-powered recommendation explanations
- Assessment comparison feature
- Out-of-scope query detection
- FastAPI REST API
- Interactive Swagger documentation
- Deployed on Railway

---

# How it Works

The application follows the workflow below:

```
User Query
     │
     ▼
Conversation Manager
     │
     ├── Ask clarification questions (if needed)
     │
     ▼
Semantic Search (FAISS)
     │
     ▼
Top Matching SHL Assessments
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Final Response
```

The conversation manager first checks whether enough information has been provided. If the role or hiring purpose is missing, the assistant asks follow-up questions instead of immediately searching.

Once enough context is available, the query is embedded using Sentence Transformers and searched against a FAISS vector index built from the SHL product catalog.

The retrieved assessments are then passed to Gemini, which generates a concise explanation while only using the retrieved results.

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| FastAPI | REST API |
| FAISS | Vector Search |
| Sentence Transformers | Text Embeddings |
| Gemini 2.5 Flash | Natural Language Generation |
| Pydantic | Request Validation |
| Railway | Deployment |

---

# Project Structure

```
shl-assessment-agent
│
├── app
│   ├── api
│   ├── core
│   ├── models
│   ├── retrieval
│   └── main.py
│
├── data
│   ├── raw
│   ├── processed
│   └── faiss
│
├── tests
│
├── requirements.txt
└── README.md
```

---

# API Endpoints

## Health Check

```
GET /health
```

Returns

```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

```
POST /chat
```

Example Request

```json
{
    "messages":[
        {
            "role":"user",
            "content":"I need an assessment for hiring a Java Developer"
        }
    ]
}
```

Example Response

```json
{
    "reply":"Recommended assessments...",
    "recommendations":[
        {
            "name":"Java 8 (New)",
            "url":"..."
        }
    ],
    "end_of_conversation":true
}
```

---

# Example Conversation

**User**

```
I need an assessment.
```

**Assistant**

```
What role are you hiring for?
```

**User**

```
Java Developer
```

**Assistant**

```
Is this for hiring, selection, employee development, or training?
```

**User**

```
Hiring
```

The assistant then retrieves the most relevant SHL assessments and explains why they are suitable.

---

# Assessment Comparison

The assistant also supports comparison requests.

Example:

```
Compare Java 8 and Core Java Advanced assessments.
```

It compares only the retrieved assessments and explains:

- Purpose
- Skills measured
- Main differences
- Suitable use cases
- Recommendation based on the hiring scenario

---

# Out-of-Scope Handling

If the user asks something unrelated to SHL assessments, the assistant politely declines.

Example:

```
Tell me a joke.
```

Response:

```
I'm designed to help with SHL assessment recommendations. Please ask about hiring, roles, skills, or assessments.
```

---

# Running the Project Locally

## Clone the repository

```bash
git clone https://github.com/jaishreeshyam7/shl-assessment-agent.git

cd shl-assessment-agent
```

## Create a virtual environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

## Generate embeddings

```bash
python app/retrieval/create_embeddings.py
```

## Start the API

```bash
uvicorn app.main:app --reload
```

Open Swagger at

```
http://127.0.0.1:8000/docs
```

---

# Design Decisions

Some design choices made while building this project:

- Used semantic search instead of keyword search to improve recommendation quality.
- Added a conversation manager to support multi-turn interactions.
- Used Gemini only for explanation generation; recommendations always come from retrieved SHL assessments.
- Included out-of-scope detection to prevent unrelated conversations.
- Kept the API stateless by passing the conversation history in every request.

---

# Possible Improvements

Given more time, I would like to extend the project with:

- Hybrid search (BM25 + FAISS)
- Better ranking using assessment metadata
- Redis-based conversation memory
- Authentication
- Streaming responses
- Multi-language support

---

## Challenges Faced

During development, I encountered a few practical challenges:

- Managing multi-turn conversations while keeping the API stateless.
- Deploying FAISS-based retrieval on cloud platforms with memory constraints.
- Ensuring Gemini generated explanations only from retrieved assessments instead of inventing recommendations.
- Balancing semantic search quality with response latency.

These challenges influenced several implementation decisions, particularly around conversation management and retrieval.

# Author

**Yash Garg**

B.Tech Mathematics and Computing

Delhi Technological University (DTU)

---

This project was developed as part of the SHL AI Intern assignment.
