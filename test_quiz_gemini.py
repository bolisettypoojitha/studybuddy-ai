import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyA1STXzc7NY5hnpacUxC5q9inRSx4iDYGk")  # Replace with your working key

model = genai.GenerativeModel("models/gemini-2.5-pro")

note_text = """
Python is a high-level programming language used for web development, automation, AI, and data analysis.
It is known for its readability and has a large standard library.
"""

prompt = f"""
Generate 2 multiple-choice questions from the following note.

Use this strict format:
Question: <question>
A. <option A>
B. <option B>
C. <option C>
D. <option D>
Answer: <A/B/C/D>

Note:
\"\"\"
{note_text}
\"\"\"
"""

response = model.generate_content(prompt)
print("📦 Gemini Response:")
print(response.text)
