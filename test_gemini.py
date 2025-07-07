import google.generativeai as genai

genai.configure(api_key="AIzaSyA1STXzc7NY5hnpacUxC5q9inRSx4iDYGk")

model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")

prompt = "Summarize the Python programming language."

try:
    response = model.generate_content(prompt)
    print("✅ Gemini Response:")
    print(response.text)
except Exception as e:
    print("❌ Gemini Error:")
    print(e)
