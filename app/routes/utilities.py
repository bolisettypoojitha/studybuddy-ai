from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Note
from app.utilities.gemini_utils import generate_summary_from_text

utilities_bp = Blueprint("utilities", __name__)

@utilities_bp.route("/generate_topic", methods=["GET", "POST"])
@login_required
def generate_topic():
    generated_content = None
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic:
            prompt = f"Explain the topic '{topic}' in a simple and clear way suitable for students."
            generated_content = generate_summary_from_text(
                prompt,
                model="gemini-2.5-pro"  # ✅ use the specified model
            )

            # 📝 Save as a note
            new_note = Note(
                subject="AI Generated",
                topic=topic,
                content=generated_content,
                user_id=current_user.id
            )
            db.session.add(new_note)
            db.session.commit()

            flash("Generated topic saved to your notes! 🎉", "success")

    return render_template("generate_topic.html", generated_content=generated_content)
