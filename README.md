# WeekLi

**The AI student review tool.** WeekLi analyzes your course syllabus and generates weekly quiz questions based on what your class is actually covering — so you stay sharp without burning out.

---

## How It Works

1. Upload your course syllabus (PDF)
2. WeekLi reads the topics, sections, and week-by-week content
3. AI generates targeted multiple-choice review questions focused on the current week's material
4. Review, study, repeat — every week

---

## Features

### Current (MVP — In Development)

- **Syllabus Upload & Analysis** — Upload a PDF syllabus; AI extracts topics, sections, and weekly content structure
- **Weekly AI-Generated Questions** — Multiple-choice review questions tailored to what your class is covering this week
- **Topic-Aware Questions** — Questions reflect the specific concepts, sections, and topics from the current week, not generic course overviews
- **Instant Results** — Questions generated in seconds via the Claude AI API

### Planned

- **Week Selector** — Choose which week's material to review, not just the latest
- **Smart Exam Mode** — AI detects upcoming exams from the syllabus and ramps up practice intensity
- **RateMyProfessor Integration** — Tailor question style to your professor's known exam patterns
- **Coursicle Integration** — Auto-populate courses by university and course number
- **Progress Tracking** — Streaks, weak area detection, and mastery scores per topic
- **Multi-device Support** — Web-first, macOS widget coming later

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React |
| Backend | FastAPI (Python) |
| AI | Claude (Anthropic API) |
| PDF Parsing | PyPDF2 |

---

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Add a `.env` file in `backend/` with your Anthropic API key:
```
ANTHROPIC_API_KEY=your_key_here
```

### Frontend

```bash
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000`, backend at `http://localhost:8000`.
