import os
import shutil
from pathlib import Path
# Updated to the new standard package
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from ast_chunker import extract_python_chunks

# Ensures vectorstore folder is created at the project root
BASE_VECTORSTORE_DIR = Path(__file__).parent.parent.absolute() / "vectorstore"

def ingest_codebase(folder_path: str, project_name: str = "default"):
    """
    Scans a folder for Python files, chunks them via AST, 
    and saves a project-specific FAISS index.
    """
    all_chunks = []
    source_path = Path(folder_path)

    if not source_path.exists():
        raise ValueError(f"Source folder does not exist: {folder_path}")

    print(f"Starting ingestion for project: {project_name}...")

    # 1. Walk through the directory
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                
                try:
                    # Attempt AST extraction (Classes/Functions)
                    chunks = extract_python_chunks(path)

                    # Fallback: If AST chunking fails or returns nothing (script style)
                    if not chunks:
                        with open(path, "r", encoding="utf-8") as f:
                            full_code = f.read()
                        
                        chunks = [{
                            "code": full_code,
                            "metadata": {"type": "full_file"}
                        }]

                    # Enrich metadata for the QA engine to use
                    for chunk in chunks:
                        chunk["metadata"].update({
                            "file": file,
                            "full_path": path,
                            "project": project_name
                        })
                    
                    all_chunks.extend(chunks)

                except Exception as e:
                    print(f"Skipping {file} due to error: {e}")

    # 2. Validation
    if not all_chunks:
        raise ValueError("No Python files were successfully processed.")

    # 3. Embedding & Vectorstore Setup
    texts = [chunk["code"] for chunk in all_chunks]
    metadatas = [chunk["metadata"] for chunk in all_chunks]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Save to Project-Specific Directory
    project_vector_path = BASE_VECTORSTORE_DIR / project_name
    
    # Clean up old index if it exists
    if project_vector_path.exists():
        shutil.rmtree(project_vector_path)
    
    # Create and save new index
    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vectorstore.save_local(str(project_vector_path))

    print(f"Ingestion complete. Indexed {len(texts)} chunks for '{project_name}'.")
    print(f"Saved to: {project_vector_path}")

    return str(project_vector_path)

# Example:
# if __name__ == "__main__":
#     ingest_codebase("./my_flutter_app", "cricket_app")