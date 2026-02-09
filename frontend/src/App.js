import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [project, setProject] = useState(null);

  const uploadProject = async () => {
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  setLoading(true);
  const response = await axios.post("http://localhost:8000/upload/", formData);
  setProject(response.data.project);   // 🔥 CRITICAL
  setLoading(false);

  alert(`Project '${response.data.project}' indexed successfully!`);
};


  const askQuestion = async () => {
  if (!question || !project) return;

  setLoading(true);

  try {
    const response = await axios.post("http://localhost:8000/ask/", {
      question: question,
      project: project
    });

    setAnswer(response.data.answer);
  } catch (error) {
    console.error("Error asking question:", error);
  }

  setLoading(false);
};
  const analyzeCode = async () => {
    setLoading(true);
    const response = await axios.post("http://localhost:8000/analyze/");
    setAnalysis(JSON.stringify(response.data.analysis, null, 2));
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Codebase Assistant</h1>

      <div className="card">
        <h3>Upload Project</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadProject}>Upload</button>
      </div>

      <div className="card">
        <h3>Ask a Question</h3>
        <textarea
          rows="3"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about the codebase..."
        />
        <button onClick={askQuestion}>Ask</button>
      </div>

      <div className="card">
        <h3>Static Analysis</h3>
        <button onClick={analyzeCode}>Analyze Code</button>
        {analysis && <pre>{analysis}</pre>}
      </div>

      {loading && <div className="loading">Thinking...</div>}

      {answer && (
        <div className="card answer">
          <h3>Answer</h3>
          <pre>{answer}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
