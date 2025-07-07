from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Note
from app.form import NoteForm
from app.utilities.gemini_utils import (
    generate_summary_from_text,
    generate_flashcards_from_text,
    generate_quiz_from_text
)

notes_bp = Blueprint('notes', __name__)

# ----------------------------------------
# View all notes
# ----------------------------------------
@notes_bp.route('/notes')
@login_required
def notes():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=user_notes)

# ----------------------------------------
# Add a new note
# ----------------------------------------
@notes_bp.route('/notes', methods=['GET', 'POST'])
@login_required
def add_note():
    if request.method == 'POST':
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        content = request.form.get('content')

        if subject and topic and content:
            new_note = Note(subject=subject, topic=topic, content=content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            print("Note added:", subject, topic, content)
            flash('Note added successfully! 🎉', 'success')
            return redirect(url_for('notes.notes'))
        else:
            print("Note form missing data:", subject, topic, content)
            flash('All fields are required!', 'danger')

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

# ----------------------------------------
# Search notes
# ----------------------------------------
@notes_bp.route('/search', methods=['GET'])
@login_required
def search_notes():
    query = request.args.get('q', '')
    user_notes = Note.query.filter(
        Note.user_id == current_user.id,
        Note.topic.ilike(f'%{query}%') | Note.subject.ilike(f'%{query}%') | Note.content.ilike(f'%{query}%')
    ).all()
    return render_template('notes.html', notes=user_notes)

# ----------------------------------------
# Edit note
# ----------------------------------------
@notes_bp.route('/notes/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('notes.notes'))

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.subject = form.subject.data
        note.topic = form.topic.data
        note.content = form.content.data
        db.session.commit()
        flash("Note updated successfully.", "success")
        return redirect(url_for('notes.notes'))

    return render_template('edit_note.html', form=form, note=note)

# ----------------------------------------
# Delete note
# ----------------------------------------
@notes_bp.route('/notes/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('notes.notes'))

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for('notes.notes'))

# ----------------------------------------
# Summarize note using Gemini
# ----------------------------------------
@notes_bp.route('/notes/summarize/<int:note_id>')
@login_required
def summarize_note(note_id):
    note = Note.query.get_or_404(note_id)
    summary = generate_summary_from_text(note.content)
    return render_template("notes_summary.html", note=note, summary=summary)

# ----------------------------------------
# Generate flashcards using Gemini
# ----------------------------------------
@notes_bp.route('/notes/flashcards/<int:note_id>')
@login_required
def generate_flashcards(note_id):
    note = Note.query.get_or_404(note_id)
    output = generate_flashcards_from_text(note.content)

    flashcards = []
    lines = output.split('\n')
    for i in range(len(lines)):
        if lines[i].startswith("Question:"):
            question = lines[i].replace("Question:", "").strip()
            if i + 1 < len(lines) and lines[i + 1].startswith("Answer:"):
                answer = lines[i + 1].replace("Answer:", "").strip()
                flashcards.append({"question": question, "answer": answer})

    return render_template("note_flashcards.html", note=note, flashcards=flashcards)

# ----------------------------------------
# Generate quiz using Gemini
# ----------------------------------------
@notes_bp.route('/generate_quiz/<int:note_id>')
@login_required
def generate_quiz(note_id):
    note = Note.query.get_or_404(note_id)
    result = generate_quiz_from_text(note.content)

    if isinstance(result, str) and result.startswith("Error"):
        return render_template("quiz.html", questions=[], error=result, note=note)

    return render_template("quiz.html", questions=result, note=note)

