from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from app.models import Note
from app.utils.gemini_api import summarize_text, generate_questions 


quiz = Blueprint('quiz', __name__)

@quiz.route("/quiz/<int:note_id>", methods=["GET"])
@login_required
def generate_quiz(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect("/notes")

    questions_data = generate_questions(note.content)

    questions = []
    for q in questions_data:
        if isinstance(q, dict) and 'question' in q and 'answer' in q:
            questions.append({
                'question': q['question'],
                'answer': q['answer']
            })

    return render_template("quiz.html", note=note, questions=questions)
