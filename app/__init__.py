from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config from instance/config.py if exists
    app.config.from_pyfile("config.py", silent=True)

    # Set secret key and DB URI
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///studybuddy.db')

    db.init_app(app)
    login_manager.init_app(app)

    # Import models so Flask-Login can use User
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register all routes
    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.notes import notes
    from app.routes.tools import tools
    from app.routes.planner import planner
    from app.routes.quiz import quiz
    from app.routes.todo import todo

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(notes)
    app.register_blueprint(tools)
    app.register_blueprint(planner)
    app.register_blueprint(quiz)
    app.register_blueprint(todo)

    return app
