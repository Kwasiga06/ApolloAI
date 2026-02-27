import os
import json
import re
from anthropic import Anthropic

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _parse_json(text):
    """Strip markdown code fences and parse JSON."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return json.loads(text.strip())


def extract_topics_from_syllabus(syllabus_text):
    """Return a list of topic/week strings extracted from the syllabus."""
    prompt = f"""You are analyzing a course syllabus. Extract only the weeks or sections that contain actual academic content students need to learn.

Return ONLY a JSON array of short topic label strings. Each label should be clear and concise (e.g. "Week 1: Newton's Laws", "Chapter 3: Cell Biology", "Topic: Thermodynamics").

EXCLUDE anything that is not a lesson, such as:
- Spring Break, Fall Break, Winter Break, or any holiday/break
- No Class, Cancelled, TBD
- Exam week, Midterm, Final Exam, Quiz day (unless the topic being examined is listed)
- Administrative weeks (e.g. syllabus review, orientation, introduction week with no content)
- Any week or section with no actual subject matter to study

Syllabus:
{syllabus_text}

Return only valid JSON — no other text. Example format:
["Week 1: ...", "Week 2: ...", "Week 3: ..."]"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    return _parse_json(message.content[0].text)


def generate_quiz_questions(syllabus_text, num_questions=5, topic=None):
    """Return a list of structured question dicts for the given topic."""
    topic_context = f" specifically on the topic: **{topic}**" if topic else " focused on the most recently covered material"

    prompt = f"""You are an expert educator generating a multiple-choice quiz{topic_context}.

Course Syllabus:
{syllabus_text}

Generate exactly {num_questions} multiple-choice questions that test conceptual understanding.

Rules:
- Do NOT ask questions about the syllabus structure itself (dates, schedules, etc.)
- Test real understanding: concepts, principles, problem-solving, application
- For STEM subjects use LaTeX: $...$ for inline math, $$...$$ for block equations

Return ONLY a JSON array — no other text. Use this exact format:
[
  {{
    "id": 1,
    "question": "question text here",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "answer": "A"
  }}
]"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    return _parse_json(message.content[0].text)


def generate_explanation(question, options, correct_answer, user_answer, topic):
    """Return an explanation for a wrong answer and a YouTube search term."""
    correct_text = options[correct_answer]
    user_text = options[user_answer]

    prompt = f"""A student answered a quiz question incorrectly. Help them understand why in a clear, encouraging way.

Topic: {topic}
Question: {question}
Student's answer: {user_answer}) {user_text}
Correct answer: {correct_answer}) {correct_text}

Write a concise explanation (2-4 sentences) of why {correct_answer} is correct and why the student's choice was a common misconception or mistake.

Return ONLY a JSON object — no other text:
{{"explanation": "..."}}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}]
    )

    return _parse_json(message.content[0].text)


if __name__ == "__main__":
    print("Quiz Question Generator Test")
    test_syllabus = """
Physics 101 - Introduction to Mechanics

    Week 1: Newton's Laws of Motion
    - First Law (Inertia)
    - Second Law (F=ma)
    - Third Law (Action-Reaction)

    Week 2: Energy and Work
    - Kinetic Energy
    - Potential Energy
    - Conservation of Energy
    """
    print("=" * 50)

    topics = extract_topics_from_syllabus(test_syllabus)
    print("Extracted topics:", topics)

    quiz_questions = generate_quiz_questions(test_syllabus, num_questions=3, topic=topics[0])
    print("\nGenerated Quiz Questions:")
    for q in quiz_questions:
        print(f"\nQ{q['id']}: {q['question']}")
        for letter, text in q['options'].items():
            print(f"  {letter}) {text}")
        print(f"  Answer: {q['answer']}")

    print("\n" + "=" * 50)
    print("Test Completed")
