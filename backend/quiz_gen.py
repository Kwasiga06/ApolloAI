from pdf_parser import extract_text_from_pdf
from ai_prod import generate_quiz_questions
import os

def generate_quiz_from_pdf(file_path, num_questions=5):
    print("🏛️ Apollo")
    print("=" * 50)

    print("\n📄 Step 1: Reading Syllabus")
    syllabus_text = extract_text_from_pdf(file_path)
    print(f"✅ Text extracted. Length: {len(syllabus_text)} characters")

    print(f"\n🧠 Step 2: Generating {num_questions} quiz questions...")
    questions = generate_quiz_questions(syllabus_text, num_questions)
    print("✅ Quiz generated successfully!")

    print("\n" + "=" * 50)
    print("YOUR QUIZ:\n")
    print(questions)

    return questions

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "test.pdf")
    quiz = generate_quiz_from_pdf(pdf_path, num_questions=5)


    output_path = os.path.join(script_dir, 'generated_quiz.txt')
    with open(output_path, 'w') as f:
        f.write(quiz)

    print(f"\nQuiz saved to {output_path}")