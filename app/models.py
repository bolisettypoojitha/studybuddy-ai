from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    # 🌟 New fields for settings
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    gender = db.Column(db.String(50))
    dob = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))




    notes = db.relationship('Note', backref='user', lazy=True)
    flashcards = db.relationship('Flashcard', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    plans = db.relationship('StudyPlan', backref='user', lazy=True)



 


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=True)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Associate with a specific user (assuming you have a User model)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_complete = db.Column(db.Boolean, default=False)  # ✅ Add this line

    def __repr__(self):
        return f"<Task {self.description[:20]}...>"



class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Planner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_done = db.Column(db.Boolean, default=False)
