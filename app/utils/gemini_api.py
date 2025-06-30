import google.generativeai as genai

genai.configure(api_key="AIzaSyCzy__IsIGjpggrYLgvAt12V-qS7sYRTKs")

# ✅ Use correct model name
model = genai.GenerativeModel("models/gemini-1.5-flash")

def summarize_text(text):
    try:
        prompt = f"Summarize the following content:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

def generate_questions(text):
    try:
        prompt = (
            f"Generate 5 quiz questions with answers based on this content:\n\n{text}\n\n"
            "Format:\nQuestion: ...\nAnswer: ..."
        )
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")
        questions = []
        q = a = ""
        for line in lines:
            if line.lower().startswith("question"):
                q = line.split(":", 1)[-1].strip()
            elif line.lower().startswith("answer"):
                a = line.split(":", 1)[-1].strip()
                if q and a:
                    questions.append({"question": q, "answer": a})
                    q, a = "", ""
        return questions if questions else [{"question": "⚠️ No questions found", "answer": ""}]
    except Exception as e:
        return [{"question": "❌ Gemini Error", "answer": str(e)}]
