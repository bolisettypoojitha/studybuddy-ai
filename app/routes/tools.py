from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Note
from app.utils.gemini_api import summarize_text, generate_questions 


tools = Blueprint('tools', __name__)

# 🕒 Pomodoro Timer route
@tools.route("/tools/timer")
@login_required
def pomodoro_timer():
    return render_template("timer.html")

# ➕ Redirect if /timer is visited directly (fixes 404)
@tools.route("/timer")
@login_required
def timer_redirect():
    return redirect(url_for("tools.pomodoro_timer"))

# 🧠 Flashcard Generator from Note ID
@tools.route("/tools/flashcards/<int:note_id>")
@login_required
def generate_flashcards(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash("Unauthorized access to note.", "danger")
        return redirect(url_for("notes.view_notes"))

    try:
        questions_data = generate_questions(note.content)
        flashcards = []

        for q in questions_data:
            if isinstance(q, dict) and 'question' in q and 'answer' in q:
                flashcards.append({
                    'question': q['question'],
                    'answer': q['answer']
                })
            elif isinstance(q, str):
                flashcards.append({
                    'question': q,
                    'answer': 'Not available'
                })

        return render_template("flashcards.html", flashcards=flashcards, note=note)

    except Exception as e:
        print("Error generating flashcards:", e)
        flash("Error generating flashcards. Please try again later.", "danger")
        return redirect(url_for("notes.view_notes"))

# 🛑 Fallback route for /flashcards (fixes 404)
@tools.route("/flashcards")
@login_required
def flashcards_landing():
    flash("⚠️ Please select a specific note to generate flashcards.", "info")
    return redirect(url_for("notes.view_notes"))
