import requests

API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-squadv2"
headers = {
    "Authorization": "Bearer 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"
}

prompt = "context: Artificial Intelligence enables machines to learn from data. question: What does AI enable machines to do?"

response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

print("Status Code:", response.status_code)
print("Response Text:", response.text)
