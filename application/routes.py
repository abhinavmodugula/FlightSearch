"""
Routes for the main functionality of the app
@author: abhin
"""

from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session, g, Blueprint
from .search import SkyScanner, get_currencies, get_location_codes

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
    currencies = get_currencies()
    curr_names_on_dropdown = []  # items to display to user on dropdown
    for i in currencies:
        curr_names_on_dropdown.append(i["Code"] + " - " + i["Symbol"])
    return render_template("home.html", curr_names=curr_names_on_dropdown[0:3], rest=curr_names_on_dropdown[3:])

@main_bp.route("/see_search_results", methods=["POST"])
def search():
    """Handles the search form inputs from the user and
    redirects to the results page"""
    currencies = get_currencies()
    curr_val = request.form["curr"]
    #convert index of selection to curr code
    if (curr_val == "1000"):
        curr_val = currencies[0]['Code']
    elif (curr_val == "1001"):
        curr_val = currencies[1]['Code']
    elif (curr_val == "1002"):
        curr_val = currencies[2]['Code']
    else:
        curr_val = currencies[3:][int(curr_val) - 1]["Code"]

    scanner = SkyScanner(currency=curr_val)
    #Next, parse the start and end locations and assign codes
    start_code = ""
    end_code = ""
    start_input = request.form["start"]
    end_input = request.form["end"]
    start_codes = get_location_codes(scanner, start_input)
    end_codes = get_location_codes(scanner, end_input)

    #Next, parse the start and end dates
    one_way = False
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    if (end_code == None):
        one_way = True

    #Now, I need to extract the cheapest Quote object and all other quote objects
    return redirect(url_for("main_bp.index"))

@main_bp.route("/results_page")
def results_page():
    pass
