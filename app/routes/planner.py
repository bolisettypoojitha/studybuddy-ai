from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Planner
from datetime import datetime

planner_bp = Blueprint('planner', __name__)

# View planner and chart
@planner_bp.route('/planner', methods=['GET'])
@login_required
def planner():
    planner_items = Planner.query.filter_by(user_id=current_user.id).order_by(Planner.date).all()
    chart_data = {}
    for item in planner_items:
        day = item.date.strftime('%A')
        chart_data[day] = chart_data.get(day, 0) + 1
    return render_template("planner.html", planner_items=planner_items, chart_data=chart_data)

# Add planner task
@planner_bp.route('/planner/add', methods=['POST'])
@login_required
def add_planner():
    title = request.form.get('title')
    description = request.form.get('description')
    date_str = request.form.get('date')

    if not (title and description and date_str):
        flash("All fields are required!", "danger")
        return redirect(url_for('planner.planner'))

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        flash("Invalid date format.", "danger")
        return redirect(url_for('planner.planner'))

    new_task = Planner(
        user_id=current_user.id,
        title=title,
        description=description,
        date=date,
        is_done=False
    )
    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!", "success")
    return redirect(url_for('planner.planner'))


# Toggle task done/undone
@planner_bp.route('/planner/toggle/<int:item_id>', methods=['POST'])
@login_required
def toggle_task(item_id):
    item = Planner.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('planner.planner'))
    item.is_done = not item.is_done
    db.session.commit()
    return redirect(url_for('planner.planner'))

# Delete planner task
@planner_bp.route('/planner/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_task(item_id):
    item = Planner.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('planner.planner'))
    db.session.delete(item)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for('planner.planner'))

# Edit planner task
@planner_bp.route('/planner/edit/<int:item_id>', methods=['POST'])
@login_required
def edit_task(item_id):
    item = Planner.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('planner.planner'))
    item.title = request.form['title']
    item.description = request.form['description']
    item.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    db.session.commit()
    flash("Task updated.", "success")
    return redirect(url_for('planner.planner'))
