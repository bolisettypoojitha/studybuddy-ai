import os
import google.generativeai as genai

# Load Gemini API key
GEMINI_API_KEY = "AIzaSyA1STXzc7NY5hnpacUxC5q9inRSx4iDYGk"


# 🔍 Debug line — print to see if the key is loaded
print("🔑 Loaded GEMINI_API_KEY in Flask:", GEMINI_API_KEY)


# Configure the model
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-pro")

def summarize_text(input_text):
    prompt = f"Summarize the following text:\n\n{input_text.strip()}"
    try:
        if not GEMINI_API_KEY:
            return "❌ Error: Gemini API key not found. Set GEMINI_API_KEY environment variable."
        
        print("⚡ Prompt sent to Gemini:\n", prompt)
        response = model.generate_content(prompt)
        print("✅ Gemini raw response:", response)

        if hasattr(response, 'text'):
            return response.text.strip()
        else:
            return "\n".join(part.text.strip() for part in response.candidates[0].content.parts)

    except Exception as e:
        print("❌ Exception during summarization:", str(e))  # 👈 print real error
        return "Error: Unable to summarize note."
