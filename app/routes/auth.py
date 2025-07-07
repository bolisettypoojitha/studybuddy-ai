from flask import Blueprint, app, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.form import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Form validated ✅")
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            login_user(user)
            print(f"User login successful: {user.email}")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))
        else:
            print("Invalid credentials ❌")
            flash('Invalid email or password', 'danger')
    else:
        if request.method == 'POST':
            print("Form failed to validate ❌")
            print(form.errors)  # this will print specific WTForms errors
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Register form validated ✅")
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User registered: {new_user.email}")
        login_user(new_user)
        return redirect(url_for('dashboard.dashboard'))
    else:
        if request.method == 'POST':
            print("Register form failed ❌")
            print(form.errors)
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
