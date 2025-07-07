from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from app.models import db, User
import os

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.bio = request.form.get('bio')
        current_user.gender = request.form.get('gender')
        current_user.dob = request.form.get('dob')
        current_user.phone = request.form.get('phone')
        current_user.location = request.form.get('location')

        # Handle profile picture upload
        profile_pic = request.files.get('profile_pic')
        if profile_pic and profile_pic.filename != '':
            upload_folder = os.path.join('app', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(profile_pic.filename)
            filepath = os.path.join(upload_folder, filename)
            profile_pic.save(filepath)
            current_user.profile_pic = filename

        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings.settings'))

    return render_template('settings.html', user=current_user)

@settings_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    logout_user()
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('auth.login'))
