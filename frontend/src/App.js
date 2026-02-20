// frontend/src/App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [questions, setQuestions] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
    setQuestions(''); // Clear previous questions
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError('');
    setQuestions('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload-syllabus', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      console.log('Response:', data); // Debug log

      if (response.ok && data.questions) {
        setQuestions(data.questions);
      } else {
        setError(data.detail || 'Failed to generate questions');
      }
    } catch (err) {
      console.error('Error:', err); // Debug log
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏛️ Apollo: AI-Powered Education</h1>
        <p>Upload your syllabus and get AI-generated quiz questions</p>
      </header>

      <div className="upload-section">
        <input 
          type="file" 
          accept=".pdf"
          onChange={handleFileChange}
        />
        <button 
          onClick={handleUpload} 
          disabled={loading}
        >
          {loading ? 'Generating Questions...' : 'Upload & Generate Quiz'}
        </button>

        {error && <p className="error">{error}</p>}
      </div>

      {questions && (
        <div className="questions-section">
          <h2>Your Quiz Questions:</h2>
          <pre>{questions}</pre>
        </div>
      )}
    </div>
  );
}

export default App;