import os
import google.generativeai as genai

# Load API key from environment
GEMINI_API_KEY = "AIzaSyA1STXzc7NY5hnpacUxC5q9inRSx4iDYGk"
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model once
model = genai.GenerativeModel("gemini-2.5-pro")

# Summary generation
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary_from_text(prompt, model="gemini-2.5-pro"):
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", e)
        return f"Error: {str(e)}"



# Flashcard generation
def generate_flashcards_from_text(content):
    prompt = (
        "Generate 10 flashcards in this format:\n"
        "Question: ...\nAnswer: ...\n\n"
        f"{content}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Flashcard Error:", e)
        return "Error: Unable to generate flashcards."

# Quiz generation
def generate_quiz_from_text(note_text):
    import os
    import google.generativeai as genai

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-2.5-pro")

    prompt = f"""
    Generate 10 multiple-choice questions from the note below.

    Format strictly:
    Question: <question>
    A. <option A>
    B. <option B>
    C. <option C>
    D. <option D>
    Answer: <A/B/C/D>

    Use line breaks. No explanations.

    Note:
    \"\"\"
    {note_text}
    \"\"\"
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        print("📦 Gemini Output:\n", raw_text)

        questions = []
        blocks = raw_text.split("Question:")

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            lines = block.splitlines()
            question = ""
            options = []
            answer = ""

            for line in lines:
                line = line.strip()
                if not question:
                    question = line
                elif line.startswith(("A.", "B.", "C.", "D.")):
                    options.append(line)
                elif line.startswith("Answer:"):
                    answer = line.replace("Answer:", "").strip()

            if question and len(options) == 4 and answer:
                questions.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })

        return questions

    except Exception as e:
        return f"Error: {str(e)}"
