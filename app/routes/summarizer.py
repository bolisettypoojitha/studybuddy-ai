from flask import Blueprint, render_template, request, flash
from app.utilities.summarizer import summarize_text

summarizer_bp = Blueprint('summarizer', __name__)

@summarizer_bp.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    summary = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text')
        if input_text:
            summary = summarize_text(input_text)
        else:
            flash("Please enter text to summarize.", "warning")
    return render_template("summarizer.html", summary=summary)
