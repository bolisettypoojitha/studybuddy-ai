
import os
from wsgiref import headers
import requests

# Load your Hugging Face API key from environment variable
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# Summarization
def summarize_text_with_hf(text, model_name="facebook/bart-large-cnn"):
    payload = {"inputs": text}
    response = requests.post(API_URL + model_name, headers=HEADERS, json=payload)
    result = response.json()
    
    if isinstance(result, list) and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        return "Error: Could not summarize the text."

# Flashcard generation (via text2text)
def generate_flashcards_with_hf(text, model_name="google/flan-t5-large"):
    prompt = f"Generate 3 flashcards from the following content:\n{text}"
    payload = {"inputs": prompt}
    response = requests.post(API_URL + model_name, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        return "Error: Could not generate flashcards."

# Question generation (optional)
def generate_questions_with_hf(text, model_name="google/flan-t5-large"):
    prompt = f"Generate 3 quiz questions from the following text:\n{text}"
    payload = {"inputs": prompt}
    response = requests.post(API_URL + model_name, headers=HEADERS, json=payload)
    result = response.json()

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        return "Error: Could not generate questions."
    
def generate_flashcards(note_text):
    prompt = f"Generate 3 flashcards from the following study notes:\n\n{note_text}\n\nFormat: Question - Answer"
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    response.raise_for_status()
    
    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    return "No flashcards generated."