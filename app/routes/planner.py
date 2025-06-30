from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from app import db
from app.models import StudyPlan

planner = Blueprint('planner', __name__)

@planner.route("/planner", methods=["GET", "POST"])
@login_required
def view_planner():
    if request.method == "POST":
        date = request.form.get("date")
        topic = request.form.get("topic")

        if not date or not topic:
            flash("Please enter both date and topic.", "warning")
            return redirect("/planner")

        new_plan = StudyPlan(date=date, topic=topic, user_id=current_user.id)
        db.session.add(new_plan)
        db.session.commit()
        flash("Study plan added!", "success")

    plans = StudyPlan.query.filter_by(user_id=current_user.id).order_by(StudyPlan.date).all()
    return render_template("planner.html", plans=plans)
