from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Task

dashboard = Blueprint('dashboard', __name__)

# === Custom Welcome Page ===
@dashboard.route("/")
def home():
    return render_template("home.html")

# === User Dashboard ===
@dashboard.route("/dashboard")
@login_required
def dashboard_home():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    total = len(user_tasks)
    done = sum(task.completed for task in user_tasks)
    progress = int((done / total) * 100) if total else 0

    return render_template(
        "dashboard.html",
        name=current_user.name,
        tasks=user_tasks,
        progress=progress
    )
