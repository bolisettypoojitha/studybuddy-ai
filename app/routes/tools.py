
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from app.models import Planner
from app.utilities.gemini_utils import generate_summary_from_text

from app.utilities.huggingface_utils import generate_flashcards
import os
import requests

tools_bp = Blueprint('tools', __name__)

# ✅ Route: Summarizer Tool
@tools_bp.route('/tools/summarizer', methods=["GET", "POST"])
@login_required
def summarizer():
    summary = None

    if request.method == 'POST':
        input_text = request.form.get('input_text')

        if input_text:
            API_KEY = os.getenv("GEMINI_API_KEY")  # Make sure this is set in your .env or system
            endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [{
                    "parts": [{"text": f"Summarize the following text:\n\n{input_text}"}]
                }]
            }

            response = requests.post(
                f"{endpoint}?key={API_KEY}",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                try:
                    summary = response.json()['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    summary = "❌ Failed to parse summary."
            else:
                summary = f"❌ Error {response.status_code}: {response.text}"

    return render_template("summarizer.html", summary=summary)


# ✅ Route: Study Timer
@tools_bp.route('/tools/timer')
@login_required
def timer():
    return render_template("timer.html")

@tools_bp.route('/tools/planner')
@login_required
def planner():
    planner_items=Planner.query.filter_by(user_id=current_user.id).order_by(Planner.date).all()
    chart_data = {}
    for item in planner_items:
        day = item.date.strftime('%A')
        chart_data[day] = chart_data.get(day, 0) + 1

    return render_template("planner.html", planner_items=planner_items, chart_data=chart_data)
