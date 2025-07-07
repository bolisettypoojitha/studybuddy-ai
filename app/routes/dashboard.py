from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Note, Task
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_name = current_user.username
    notes_count = Note.query.filter_by(user_id=current_user.id).count()
    pending_tasks = Task.query.filter_by(user_id=current_user.id, is_complete=False).all()
    return render_template('dashboard.html', user_name=user_name, notes_count=notes_count, pending_tasks=pending_tasks)
