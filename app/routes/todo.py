from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task
from flask_login import login_required, current_user

todo_bp = Blueprint('todo', __name__)


# View & Add Tasks
@todo_bp.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    user_id = current_user.id

    if request.method == 'POST':
        description = request.form['description']
        new_task = Task(description=description, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('todo.todo'))

    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
    return render_template("todo.html", tasks=tasks)

# Mark as Complete
@todo_bp.route('/todo/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('todo.todo'))
    task.completed = True
    db.session.commit()
    flash('Task marked as completed!', 'info')
    return redirect(url_for('todo.todo'))

# Delete Task
@todo_bp.route('/todo/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("Unauthorized", "danger")
        return redirect(url_for('todo.todo'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'danger')
    return redirect(url_for('todo.todo'))
