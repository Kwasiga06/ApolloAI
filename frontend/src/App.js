// frontend/src/App.js — WeekLi
import React, { useState, useRef } from 'react';
import './App.css';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// Matches $$block math$$ first, then $inline math$
const MATH_REGEX = /(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/g;

function MathText({ text }) {
  const parts = text.split(MATH_REGEX);

  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('$$') && part.endsWith('$$')) {
          const html = katex.renderToString(part.slice(2, -2), { displayMode: true, throwOnError: false });
          return <span key={i} className="math-block" dangerouslySetInnerHTML={{ __html: html }} />;
        }
        if (part.startsWith('$') && part.endsWith('$')) {
          const html = katex.renderToString(part.slice(1, -1), { throwOnError: false });
          return <span key={i} dangerouslySetInnerHTML={{ __html: html }} />;
        }
        return part.split('\n').map((line, j, arr) => (
          <React.Fragment key={`${i}-${j}`}>
            {line}
            {j < arr.length - 1 && <br />}
          </React.Fragment>
        ));
      })}
    </>
  );
}

function App() {
  const [file, setFile] = useState(null);
  // step: 'upload' | 'topics' | 'quiz' | 'results'
  const [step, setStep] = useState('upload');
  const [syllabusText, setSyllabusText] = useState('');
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  // explanations: { [questionId]: { loading, text, searchTerm, error } }
  const [explanations, setExplanations] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  // Step 1: Upload PDF → extract topics
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file first');
      return;
    }
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload-syllabus', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (response.ok && data.topics) {
        setSyllabusText(data.syllabus_text);
        setTopics(data.topics);
        setStep('topics');
      } else {
        setError(data.detail || 'Failed to parse syllabus');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Select topic → generate quiz
  const handleTopicSelect = async (topic) => {
    setSelectedTopic(topic);
    setLoading(true);
    setError('');
    setAnswers({});

    try {
      const response = await fetch('http://localhost:8000/api/generate-quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ syllabus_text: syllabusText, topic, num_questions: 5 }),
      });
      const data = await response.json();

      if (response.ok && data.questions) {
        setQuestions(data.questions);
        setStep('quiz');
      } else {
        setError(data.detail || 'Failed to generate quiz');
      }
    } catch (err) {
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Step 3: Answer selection
  const handleAnswerChange = (questionId, option) => {
    setAnswers(prev => ({ ...prev, [questionId]: option }));
  };

  const allAnswered = questions.length > 0 && Object.keys(answers).length === questions.length;

  const handleSubmit = () => {
    setStep('results');
  };

  const score = questions.filter(q => answers[q.id] === q.answer).length;

  // Step 4: Fetch explanation for a wrong answer
  const handleExplain = async (q) => {
    setExplanations(prev => ({ ...prev, [q.id]: { loading: true } }));
    try {
      const response = await fetch('http://localhost:8000/api/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: q.question,
          options: q.options,
          correct_answer: q.answer,
          user_answer: answers[q.id],
          topic: selectedTopic,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setExplanations(prev => ({ ...prev, [q.id]: { loading: false, text: data.explanation } }));
      } else {
        setExplanations(prev => ({ ...prev, [q.id]: { loading: false, error: true } }));
      }
    } catch {
      setExplanations(prev => ({ ...prev, [q.id]: { loading: false, error: true } }));
    }
  };

  const handleBackToTopics = () => {
    setStep('topics');
    setSelectedTopic('');
    setQuestions([]);
    setAnswers({});
    setExplanations({});
  };

  const handleStartOver = () => {
    setStep('upload');
    setFile(null);
    setSyllabusText('');
    setTopics([]);
    setSelectedTopic('');
    setQuestions([]);
    setAnswers({});
    setError('');
  };

  return (
    <div className="App">
      <header className="App-header">
        <span className="badge">✦ AI Weekly Review</span>
        <h1>WeekLi</h1>
        <p>Upload your syllabus, pick a topic, and test your knowledge with AI-generated questions.</p>
      </header>

      {/* ── Step 1: Upload ── */}
      {step === 'upload' && (
        <div className="upload-section">
          <span className="upload-label">Your syllabus (PDF)</span>

          <div className="file-drop-area" onClick={() => fileInputRef.current.click()}>
            <span className="file-icon">📄</span>
            <span className={`file-name ${file ? 'selected' : ''}`}>
              {file ? file.name : 'Click to choose a PDF file'}
            </span>
          </div>
          <input
            type="file"
            accept=".pdf"
            ref={fileInputRef}
            onChange={handleFileChange}
          />

          <button onClick={handleUpload} disabled={loading}>
            {loading && <span className="spinner" />}
            {loading ? 'Parsing syllabus...' : 'Upload Syllabus'}
          </button>

          {error && <p className="error">{error}</p>}
        </div>
      )}

      {/* ── Step 2: Topic Selection ── */}
      {step === 'topics' && (
        <div className="topics-section">
          <div className="section-header">
            <h2>Select a Topic</h2>
            <p>Choose what you want to be quizzed on.</p>
          </div>

          {loading ? (
            <div className="loading-row">
              <span className="spinner" />
              <span>Generating quiz for <strong>{selectedTopic}</strong>…</span>
            </div>
          ) : (
            <div className="topics-grid">
              {topics.map((topic, i) => (
                <button
                  key={i}
                  className="topic-card"
                  onClick={() => handleTopicSelect(topic)}
                >
                  <span className="topic-number">{i + 1}</span>
                  <span className="topic-name">{topic}</span>
                </button>
              ))}
            </div>
          )}

          {error && <p className="error">{error}</p>}

          <button className="ghost-btn" onClick={handleStartOver}>
            ← Upload a different syllabus
          </button>
        </div>
      )}

      {/* ── Step 3: Quiz ── */}
      {step === 'quiz' && (
        <div className="quiz-section">
          <div className="section-header">
            <h2>{selectedTopic}</h2>
            <span className="questions-count">{questions.length} questions</span>
          </div>

          <div className="questions-list">
            {questions.map((q, qi) => (
              <div key={q.id} className="question-card">
                <div className="question-text">
                  <span className="q-num">Q{qi + 1}</span>
                  <div className="q-body"><MathText text={q.question} /></div>
                </div>

                <div className="options-list">
                  {Object.entries(q.options).map(([letter, text]) => (
                    <label
                      key={letter}
                      className={`option-label ${answers[q.id] === letter ? 'selected' : ''}`}
                    >
                      <input
                        type="radio"
                        name={`q-${q.id}`}
                        value={letter}
                        checked={answers[q.id] === letter}
                        onChange={() => handleAnswerChange(q.id, letter)}
                      />
                      <span className="option-letter">{letter}</span>
                      <div className="option-text"><MathText text={text} /></div>
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="quiz-actions">
            <button onClick={handleSubmit} disabled={!allAnswered}>
              {allAnswered ? 'Submit Answers' : `Answer all questions (${Object.keys(answers).length}/${questions.length})`}
            </button>
            <button className="ghost-btn" onClick={handleBackToTopics}>
              ← Back to topics
            </button>
          </div>
        </div>
      )}

      {/* ── Step 4: Results ── */}
      {step === 'results' && (
        <div className="results-section">
          <div className="score-card">
            <div className="score-fraction">{score} <span className="score-denom">/ {questions.length}</span></div>
            <div className="score-pct">{Math.round((score / questions.length) * 100)}% correct</div>
          </div>

          <div className="questions-list">
            {questions.map((q) => {
              const userAnswer = answers[q.id];
              const correct = userAnswer === q.answer;
              return (
                <div key={q.id} className={`question-card ${correct ? 'result-correct' : 'result-incorrect'}`}>
                  <div className="question-text">
                    <span className={`q-num result-icon ${correct ? 'correct' : 'incorrect'}`}>
                      {correct ? '✓' : '✗'}
                    </span>
                    <div className="q-body"><MathText text={q.question} /></div>
                  </div>

                  <div className="options-list">
                    {Object.entries(q.options).map(([letter, text]) => (
                      <div
                        key={letter}
                        className={`option-label static
                          ${letter === q.answer ? 'answer-correct' : ''}
                          ${letter === userAnswer && !correct ? 'answer-wrong' : ''}
                        `}
                      >
                        <span className="option-letter">{letter}</span>
                        <div className="option-text"><MathText text={text} /></div>
                      </div>
                    ))}
                  </div>

                  {!correct && (
                    <div className="explanation-section">
                      <p className="answer-note">
                        Correct answer: <strong>{q.answer}</strong>
                      </p>

                      {!explanations[q.id] && (
                        <button className="explain-btn" onClick={() => handleExplain(q)}>
                          Why was I wrong?
                        </button>
                      )}

                      {explanations[q.id]?.loading && (
                        <div className="loading-row explain-loading">
                          <span className="spinner" />
                          <span>Getting explanation…</span>
                        </div>
                      )}

                      {explanations[q.id]?.text && (
                        <div className="explanation-box">
                          <p className="explanation-text">{explanations[q.id].text}</p>
                        </div>
                      )}

                      {explanations[q.id]?.error && (
                        <p className="error" style={{ marginTop: 8 }}>Couldn't load explanation. Try again.</p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <div className="quiz-actions">
            <button onClick={handleBackToTopics}>Try another topic</button>
            <button className="ghost-btn" onClick={handleStartOver}>Upload new syllabus</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
