from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import ast
from ingestion import ingest_codebase
from retriever import initialize_qa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.abspath("../project_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str
    project: str


@app.post("/upload/")
async def upload_project(file: UploadFile = File(...)):
    project_name = file.filename.replace(".py", "")

    # Always use the same upload directory
    upload_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(upload_path, "wb") as buffer:
        buffer.write(await file.read())

    vectorstore_path = ingest_codebase(UPLOAD_DIR, project_name)

    return {
        "message": "Upload successful",
        "project": project_name,
        "vectorstore_path": vectorstore_path
    }

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    qa = initialize_qa(request.project)
    response = qa.invoke(request.question)
    return {"answer": response["result"]}


@app.post("/analyze/")
async def analyze_code():
    issues = []

    for root, _, files in os.walk(UPLOAD_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    source = f.read()

                tree = ast.parse(source)

                for node in ast.walk(tree):

                    # Bare except
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        issues.append(f"{file}: Bare except detected")

                    # eval usage
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id == "eval":
                            issues.append(f"{file}: Use of eval() detected")

                    # Long functions
                    if isinstance(node, ast.FunctionDef):
                        if node.end_lineno - node.lineno > 100:
                            issues.append(f"{file}: Function '{node.name}' is too long")

    if not issues:
        return {"analysis": "No obvious structural issues detected."}

    return {"analysis": issues}
