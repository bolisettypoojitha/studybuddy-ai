from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db
from app.routes.todo import preload_tasks_for_user  # Add this import at the top


auth = Blueprint('auth', __name__)

# === Registration Route ===
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered!", category='error')
            return redirect(url_for("auth.register"))

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')  # ✅ fixed here
        )
        db.session.add(new_user)
        db.session.commit()
        preload_tasks_for_user(new_user.id)
        flash("Account created!", category='success')
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# === Login Route ===
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Incorrect login credentials.", category='error')
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("dashboard.dashboard_home"))

    return render_template("login.html")

# === Logout Route ===
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
