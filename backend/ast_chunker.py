import ast

def extract_python_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start_line = node.lineno - 1
            end_line = node.end_lineno
            code = "\n".join(source.splitlines()[start_line:end_line])

            chunks.append({
                "type": type(node).__name__,
                "name": node.name,
                "code": code,
                "metadata": {
                    "file": file_path,
                    "name": node.name,
                    "type": type(node).__name__
                }
            })

    return chunks
