import requests
import os

# ✅ Your actual Hugging Face API token (hardcoded for now)
HUGGINGFACE_API_KEY = "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"

headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}



# === Summarization Function ===
def summarize_text(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        result = response.json()

        if isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text']
        elif isinstance(result, dict) and 'error' in result:
            return f"❌ API Error: {result['error']}"
        else:
            return "⚠️ Could not generate summary. Try with more detailed input."
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# === Flashcard/Question Generator Function ===
def generate_questions(text):
    API_URL = "https://api-inference.huggingface.co/models/valhalla/t5-small-e2e-qg"
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        print("🧠 Status Code:", response.status_code)
        print("🧠 Raw Response:", response.text)

        result = response.json()

        if isinstance(result, list):
            return [{"question": item.get("question", ""), "answer": item.get("answer", "")} for item in result]
        elif isinstance(result, dict) and 'error' in result:
            return [{"question": "API Error", "answer": result['error']}]
        else:
            return [{"question": "⚠️ Could not generate questions", "answer": ""}]
    except Exception as e:
        return [{"question": "❌ Unexpected Error", "answer": str(e)}]
    

