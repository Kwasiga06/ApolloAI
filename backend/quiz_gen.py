from pdf_parser import extract_text_from_pdf
from ai_prod import extract_topics_from_syllabus, generate_quiz_questions
import os
import json


def generate_quiz_from_pdf(file_path, num_questions=5, topic=None):
    print("📅 WeekLi")
    print("=" * 50)

    print("\n📄 Step 1: Reading Syllabus")
    syllabus_text = extract_text_from_pdf(file_path)
    print(f"✅ Text extracted. Length: {len(syllabus_text)} characters")

    if topic is None:
        print("\n🗂  Step 2: Extracting topics...")
        topics = extract_topics_from_syllabus(syllabus_text)
        print(f"✅ Found {len(topics)} topics:")
        for i, t in enumerate(topics, 1):
            print(f"  {i}. {t}")
        topic = topics[0]
        print(f"\n→ Using first topic: {topic}")

    print(f"\n🧠 Step 3: Generating {num_questions} quiz questions for '{topic}'...")
    questions = generate_quiz_questions(syllabus_text, num_questions, topic)
    print("✅ Quiz generated successfully!")

    print("\n" + "=" * 50)
    print("YOUR QUIZ:\n")
    for q in questions:
        print(f"Q{q['id']}: {q['question']}")
        for letter, text in q['options'].items():
            print(f"  {letter}) {text}")
        print(f"  Answer: {q['answer']}\n")

    return questions


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "test.pdf")
    quiz = generate_quiz_from_pdf(pdf_path, num_questions=5)

    output_path = os.path.join(script_dir, 'generated_quiz.json')
    with open(output_path, 'w') as f:
        json.dump(quiz, f, indent=2)

    print(f"\nQuiz saved to {output_path}")
