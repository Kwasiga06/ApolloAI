import os
from anthropic import Anthropic

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_quiz_questions(syllabus_text, num_questions=5):
    prompt = f"""You are an expert educator creating quiz questions for college students.

    Below is a course syllabus that outlines the topics and concepts that will be taught in the course.
    Your task is to generate {num_questions} multiple-choice quiz questions that test students' understanding of the ACTUAL COURSE CONTENT and key concepts mentioned in the syllabus.

    IMPORTANT:
    - DO NOT generate questions ABOUT the syllabus itself (e.g., "What topic is covered in Week 1?")
    - DO generate questions that test understanding of the concepts, principles, and topics that are listed in the syllabus
    - Questions should test conceptual understanding, problem-solving, and application of the material that will be taught
    - Use the syllabus as a guide to understand what topics to create questions about

    Course Syllabus:
    {syllabus_text}

    Please format each question as:
    Question [number]: [question text]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Answer: [correct option letter]

    Generate questions that test deep understanding of the concepts, not questions about the syllabus structure or schedule."""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

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

    quiz_questions = generate_quiz_questions(test_syllabus, num_questions=3)

    print("Generated Quiz Questions:")
    print(quiz_questions)
    print("\n " + "=" * 50)
    print("Test Completed")



