import os
from pathlib import Path
from typing import Optional

# Updated imports for modern LangChain standards
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Global cache to prevent re-loading models into memory on every call
_embeddings: Optional[HuggingFaceEmbeddings] = None
_qa_chains: dict = {}

BASE_VECTORSTORE_DIR = Path(__file__).parent.parent.absolute() / "vectorstore"

def get_embeddings():
    """Singleton pattern for embeddings to save GPU/RAM memory."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings

def initialize_qa(project_name: str = "default"):
    """
    Initializes or retrieves a cached QA chain for a specific project.
    
    Args:
        project_name: The folder name inside 'vectorstore/' to load.
    """
    global _qa_chains

    # Return cached chain if it exists for this project
    if project_name in _qa_chains:
        return _qa_chains[project_name]

    # 1. Setup Pathing
    # Uses absolute path logic to ensure it runs from any subdirectory
    project_path = BASE_VECTORSTORE_DIR / project_name
    
    if not project_path.exists():
        raise FileNotFoundError(f"Vectorstore not found at: {project_path}")

    # 2. Load Vectorstore
    vectorstore = FAISS.load_local(
    str(project_path),
    get_embeddings()
    )

    # 3. Configure LLM
    llm=Ollama(model="phi3")

    # 4. Define Professional Prompt Template
    template = """
You are a professional code analysis assistant.

Use ONLY the provided context to answer. If the answer is not in the context, 
state that you do not have enough information.

Provide answer in this structure:
1. Purpose
2. How it works
3. Important details
4. Source Files

Context:
{context}

Question:
{question}

Answer:
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    # 5. Create Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    # Cache and return
    _qa_chains[project_name] = qa_chain
    return qa_chain

# Example Usage:
# if __name__ == "__main__":
#     chain = initialize_qa("my_flutter_project")
#     response = chain.invoke("How does the HomeController work?")
#     print(response["result"])