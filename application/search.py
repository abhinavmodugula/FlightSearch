# -*- coding: utf-8 -*-
import datetime
import json
import requests
import os
from .secret import rapidapi_key
"""
This file has helper methods to 
interact with the SkyScanner API
to search for flight quotes, locations,
and other info

"""

headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': rapidapi_key,
}

class SkyScanner:
    """ Class to interact with the SkyScanner API and
    retrieve the raw JSON output"""
    
    def __init__(self, originCountry = "US", currency = "USD", locale="en-US"):
        """Creates a SkyScanner object with default country, currency, and local
        which can be changed as necessary. In addition, a requests session is made."""
        self.originCountry = originCountry
        self.currency = currency
        self.locale = locale
        self.rootURL = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com" #path to the API
        self.airports = {}
        self.quotes = []
        self.places = []
        self.carriers = []
        
        #Create session
        self.session = requests.Session()
        self.session.headers.update(headers)
     
    def get_quotes_oneway(self, source, destination, outboundDate):
        """Gets the quotes for two specific dates. Only for 1-way trips.
        Returns both 1) quotes in JSON format and 2) a dict of airport_code -> airport_name"""
        quoteRequestPath = "/apiservices/browsequotes/v1.0/"
        browseQuotesURL = self.rootURL + quoteRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/" + source + "/" + destination + "/" + outboundDate + "/"
        response = self.session.get(browseQuotesURL)
        resultJSON = json.loads(response.text)
        
        if("Quotes" in resultJSON):
            self.quotes.append(resultJSON["Quotes"])    
            for Places in resultJSON["Places"]:
            # Add the airport in the dictionary.
                self.airports[Places["PlaceId"]] = Places["Name"]
        
        return self.quotes, self.airports
    
    #TODO: if above works, add methods so dates can also be an entire month or a custom range
    
    def search_places(self, search, country="True", city="True"):
        """Returns places that match a specific search query.
        Can choose to exclude countries or cities. Airports are
        always returned."""
        params = {}
        params["query"] = search
        params["includeCities"] = city
        params["includeCountries"] = country
        placeRequestPath = "/apiservices/autosuggest/v1.0/"
        browsePlacesURL = self.rootURL + placeRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/"
        response = self.session.get(browsePlacesURL, params=params)
        resultJSON = json.loads(response.text)
        return resultJSON

def get_currencies():
    """Returns an array of all currencies
    supported. USD, EUR, GPD are the first three"""
    here = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(here, "currencies.json")
    with open(data_path) as f:
        data = json.load(f)
    curr_array = [0] * 152 #152 total currenies
    for i in range(152):
        curr_array[i] = data['Currencies'][i]

    #move the three common ones to the front
    swap_front = [139, 43, 45]
    counter = 0
    for i in swap_front:
        tmp = curr_array[counter]
        curr_array[counter] = data['Currencies'][i]
        curr_array[i] = tmp
        counter += 1

    return curr_array

def get_location_codes(scanner, input):
    """Take user input and convert to location code
    which can be used in the API"""
    matches = scanner.search_places(input)
    codes = []
    for i in matches["Places"]:
        codes.append(i["PlaceId"])
    return codes



def string_to_date(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d").date()

class Quote():
    def __init__(self, start_time, start_air, end_air, price):
        self.company = ""
        self.start_time = start_time
        self.start_airport = start_air
        self.end_airport = end_air
        self.price = price

def get_quotes(scanner: SkyScanner, start, end, start_date, entire_month="false"):
    """Returns the cheapest quote and then all other quotes
    given the params and a scanner object"""
    all_quotes = []
    if entire_month == "false":
        quotes, airports = scanner.get_quotes_oneway(start, end, start_date)
    else:
        start_date = start_date.split("-")[0] + "-" + start_date.split("-")[1]
        quotes, airports = scanner.get_quotes_oneway(start, end, start_date)
    print(quotes)
    for quote in quotes[0]:
        price = quote['MinPrice']
        start_airport = airports[quote['OutboundLeg']["OriginId"]]
        end_airport = airports[quote['OutboundLeg']["DestinationId"]]
        start_time = quote['OutboundLeg']["DepartureDate"].split("T")[0]
        all_quotes.append(Quote(start_time, start_airport, end_airport, price))
    cheapest_price = 9999999999999
    cheapest_quote = None
    cheapest_index = None

    for i, quote in enumerate(all_quotes):
        if quote.price < cheapest_price:
            cheapest_price = quote.price
            cheapest_quote = quote
            cheapest_index = i

    if cheapest_index is not None:
        del all_quotes[cheapest_index]
    return cheapest_quote, all_quotes, airports
        
        
    
    
