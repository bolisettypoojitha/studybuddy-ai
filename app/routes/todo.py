from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Task
from app import db

todo = Blueprint('todo', __name__)

@todo.route("/todo")
@login_required
def todo_list():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("todo.html", tasks=tasks)

@todo.route("/todo/add", methods=["POST"])
@login_required
def add_task():
    description = request.form.get("description")
    if description:
        new_task = Task(description=description, completed=False, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash("✅ Task added!", "success")
    else:
        flash("⚠️ Task description cannot be empty.", "warning")
    return redirect(url_for("todo.todo_list"))

@todo.route("/todo/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for("todo.todo_list"))

@todo.route("/todo/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("todo.todo_list"))

@todo.route("/todo/add-defaults", methods=["POST"])
@login_required
def add_defaults():
    preload_tasks_for_user(current_user.id)
    flash("📋 Study tasks added!", "success")
    return redirect(url_for("todo.todo_list"))

# Utility function to preload study tasks
def preload_tasks_for_user(user_id):
    default_tasks = [
        "Complete Python module",
        "Revise AI & ML concepts",
        "Summarize notes on Cybersecurity",
        "Generate flashcards for Java basics",
        "Attempt quiz from previous notes",
        "Study 1 hour using Pomodoro timer",
        "Add AIML weekly goals to planner",
        "Prepare assignment for internship",
        "Review flashcards before quiz",
        "Take a break & drink water 💧"
    ]
    for desc in default_tasks:
        task = Task(description=desc, completed=False, user_id=user_id)
        db.session.add(task)
    db.session.commit()
