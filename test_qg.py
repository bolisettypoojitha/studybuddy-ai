import os
from app.utils import huggingface_api
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env

sample_text = """
Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction. AI is used in applications like natural language processing, robotics, and machine vision.
"""

print("📌 Summary:")
print(huggingface_api.summarize_text(sample_text))

print("\n🧠 Questions:")
questions = huggingface_api.generate_questions(sample_text)
for q in questions:
    print("Q:", q.get("question"))
    print("A:", q.get("answer"))
    print("---")
