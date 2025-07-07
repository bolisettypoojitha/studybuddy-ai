from flask import Blueprint, render_template
from flask_login import login_required
from dotenv import load_dotenv
load_dotenv()

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def home():
    return render_template('base.html')
