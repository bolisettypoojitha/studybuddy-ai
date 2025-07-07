from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os
load_dotenv()


# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Secret key and database config
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Pooji@localhost/studybuddy')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('config.DevelopmentConfig')  # Use ProductionConfig for deployment


    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    # Setup login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # User loader
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.notes import notes_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.main import main_bp
    from app.routes.home import home_bp
    from app.routes.tools import tools_bp
    from app.routes.summarizer import summarizer_bp
    from app.routes.planner import planner_bp
    from app.routes.todo import todo_bp
    from app.routes.utilities import utilities_bp
    from app.routes.settings import settings_bp





    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(tools_bp, url_prefix='/tools')
    app.register_blueprint(summarizer_bp)
    app.register_blueprint(planner_bp, url_prefix='/tools')
    app.register_blueprint(todo_bp)
    app.register_blueprint(utilities_bp)
    app.register_blueprint(settings_bp)



    return app

