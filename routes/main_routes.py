# advanced/routes/main_routes.py
from flask import Blueprint, render_template
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template("main.html")

@main_bp.route('/section/<folder>/<page>')
def section(folder, page):
    template_path = f"contents/{folder}/{page}.html"
    if os.path.exists(f"templates/{template_path}"):
        return render_template(template_path,folder=folder)
    else:
        return "페이지 없음", 404