"""
Routes for the main functionality of the app
@author: abhin
"""

from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session, g, Blueprint
from .search import SkyScanner

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route("/")
def index():
    """
    Displays the main page which has the fully-featured
    search box with multiple options

    """
    return render_template("home.html")