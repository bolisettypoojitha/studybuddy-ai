from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note
from app.utils.huggingface_api import summarize_text

notes = Blueprint('notes', __name__)

@notes.route("/notes")
@login_required
def view_notes():
    all_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=all_notes)

@notes.route("/notes/add", methods=["POST"])
@login_required
def add_note():
    subject = request.form.get("subject")
    topic = request.form.get("topic")
    content = request.form.get("content")
    new_note = Note(subject=subject, topic=topic, content=content, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    flash("Note added successfully!", "success")
    return redirect(url_for("notes.view_notes"))

@notes.route("/notes/delete/<int:note_id>")
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("Not authorized", "danger")
        return redirect(url_for("notes.view_notes"))
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("notes.view_notes"))

@notes.route("/notes/summarize/<int:note_id>")
@login_required
def summarize_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("Not authorized", "danger")
        return redirect(url_for("notes.view_notes"))
    summary = summarize_text(note.content)
    return render_template("summary.html", note=note, summary=summary)
