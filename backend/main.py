from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pdf_parser import extract_text_from_pdf
from ai_prod import extract_topics_from_syllabus, generate_quiz_questions, generate_explanation
import os
import shutil

app = FastAPI(title="WeekLi API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuizRequest(BaseModel):
    syllabus_text: str
    topic: str = None
    num_questions: int = 5


class ExplainRequest(BaseModel):
    question: str
    options: dict
    correct_answer: str
    user_answer: str
    topic: str


@app.get("/")
def read_root():
    return {"message": "WeekLi API is running", "version": "1.0.0"}


@app.post("/api/upload-syllabus")
async def upload_syllabus(file: UploadFile = File()):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        syllabus_text = extract_text_from_pdf(file_location)
        topics = extract_topics_from_syllabus(syllabus_text)
        return {"topics": topics, "syllabus_text": syllabus_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_location)


@app.post("/api/generate-quiz")
async def generate_quiz(request: QuizRequest):
    try:
        questions = generate_quiz_questions(
            request.syllabus_text,
            request.num_questions,
            request.topic,
        )
        return {"success": True, "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/explain")
async def explain_answer(request: ExplainRequest):
    try:
        result = generate_explanation(
            request.question,
            request.options,
            request.correct_answer,
            request.user_answer,
            request.topic,
        )
        return {"success": True, "explanation": result["explanation"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
