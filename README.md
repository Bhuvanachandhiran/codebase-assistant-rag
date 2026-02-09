# Codebase Assistant (Multi-Project RAG)

A Retrieval-Augmented Generation (RAG) system that allows users to upload Python projects and query them using an LLM.

## Features
- Multi-project vectorstore namespaces
- AST-based Python chunking
- FAISS vector database
- Ollama LLM integration
- Static code analysis module

## Tech Stack
- FastAPI
- React
- FAISS
- HuggingFace Embeddings
- Ollama
- LangChain

## Architecture
Upload → AST Chunking → Embedding → FAISS → Retriever → LLM → Structured Answer

# 🚀 Codebase Assistant – Setup & Run Guide

This project consists of:

- FastAPI Backend (RAG + FAISS)
- Ollama Local LLM (phi3 / llama3)
- React Frontend

---

## 1️⃣ Install Ollama

Download and install Ollama:

https://ollama.com

Pull the model:

```bash
ollama pull phi3
```

Test:

```bash
ollama run phi3
```

Keep Ollama running in background.

---

## 2️⃣ Run Backend

```bash
cd backend
python -m venv venv
```

Activate environment:

Windows:
```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## 3️⃣ Run Frontend

Open new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🔎 How It Works

1. Upload Python file
2. Code is chunked using AST
3. Embeddings created using sentence-transformers
4. FAISS vector index stored per project
5. RetrievalQA fetches relevant code
6. Ollama LLM generates structured answer

---

## Future Improvements
- Multi-language support
- Cloud deployment
- Hallucination control
