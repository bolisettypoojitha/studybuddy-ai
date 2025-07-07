import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyA1STXzc7NY5hnpacUxC5q9inRSx4iDYGk"
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-pro")

def generate_quiz_from_text(note_text):
    prompt = f"""
    Generate 10 multiple-choice questions based on the following text. 
    Format them clearly with:
    - Question
    - 4 Options (A–D)
    - Answer

    Text:
    {note_text}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Parse questions from Gemini response
        questions = []
        current_question = {}
        for line in raw_text.split("\n"):
            line = line.strip()
            if line.lower().startswith("question"):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": line, "options": [], "answer": ""}
            elif any(line.startswith(opt) for opt in ["A.", "B.", "C.", "D."]):
                current_question["options"].append(line)
            elif line.lower().startswith("answer"):
                current_question["answer"] = line.split(":", 1)[1].strip()

        if current_question:
            questions.append(current_question)

        return questions

    except Exception as e:
        return f"Error: {str(e)}"
