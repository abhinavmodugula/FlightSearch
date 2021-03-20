"""
Routes for the main functionality of the app
@author: abhin
"""

from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session, g, Blueprint
from .search import SkyScanner, get_currencies, get_location_codes, get_quotes

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

class Data:
    cheapest = None
    all_quotes = None
    airports = None
    curr_symbol = None
    start_in = None
    end_in = None

sess = Data()

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
        curr_symbol = currencies[0]['Symbol']
    elif (curr_val == "1001"):
        curr_val = currencies[1]['Code']
        curr_symbol = currencies[1]['Symbol']
    elif (curr_val == "1002"):
        curr_val = currencies[2]['Code']
        curr_symbol = currencies[2]['Symbol']
    else:
        i = int(curr_val) - 1
        curr_val = currencies[3:][i]["Code"]
        curr_symbol = currencies[3:][i]["Symbol"]

    scanner = SkyScanner(currency=curr_val)
    #Next, parse the start and end locations and assign codes
    start_code = ""
    end_code = ""
    start_input = request.form["start"]
    end_input = request.form["end"]
    start_codes = get_location_codes(scanner, start_input)
    end_codes = get_location_codes(scanner, end_input)

    #Next, parse the start date
    start_date = request.form["start_date"]
    try:
        entire_month = request.form["checkbox"]
    except:
        entire_month = "false"

    #Now, I need to extract the cheapest Quote object and all other quote objects
    cheapest, all_quotes, airports = get_quotes(scanner, start_codes[0], end_codes[0], start_date, entire_month)

    #Return error if no quotes found
    if len(all_quotes) == 0:
        return redirect(url_for("main_bp.no_results"))

    return results_page(cheapest, all_quotes, airports, curr_symbol, start_input, end_input)

@main_bp.route("/results_page")
def results_page(cheapest, all_quotes, airports, curr_symbol, start_in, end_in):
    sess.cheapest = cheapest
    sess.all_quotes = all_quotes
    sess.airports = airports
    sess.curr_symbol = curr_symbol
    sess.start_in = start_in
    sess.end_in = end_in
    start = start_in
    end = end_in
    return render_template("results.html", cheapest=cheapest, all_quotes=all_quotes, curr=curr_symbol, s=start, e=end, rev=False)

@main_bp.route("/results_page_rev")
def results_page_rev():
    start = sess.start_in
    end = sess.end_in
    if sess.all_quotes is not None:
        sess.all_quotes.reverse()
    return render_template("results.html", cheapest=sess.cheapest, all_quotes=sess.all_quotes, curr=sess.curr_symbol, s=start, e=end, rev=True)

@main_bp.route("/results_page_rev_back")
def results_page_rev_back():
    start = sess.start_in
    end = sess.end_in
    if sess.all_quotes is not None:
        sess.all_quotes.reverse()
    return render_template("results.html", cheapest=sess.cheapest, all_quotes=sess.all_quotes, curr=sess.curr_symbol, s=start, e=end, rev=False)

@main_bp.route("/no_results")
def no_results():
    return render_template("no_res.html")
