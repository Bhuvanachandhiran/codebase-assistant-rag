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

## Run Locally
1. Install backend requirements
2. Start Ollama
3. Run uvicorn
4. Start frontend

## Future Improvements
- Multi-language support
- Cloud deployment
- Hallucination control
