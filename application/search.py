# -*- coding: utf-8 -*-
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
        browseQuotesURL = self.rootURL + quoteRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/" + source + "/" + destination + "/" + outboundDate.strftime("%Y-%m-%d") + "/"
        response = self.session.get(browseQuotesURL)
        resultJSON = json.loads(response.text)
        
        if("Quotes" in resultJSON):
            self.quotes.append(resultJSON["Quotes"])    
            for Places in resultJSON["Places"]:
            # Add the airport in the dictionary.
                self.airports[Places["PlaceId"]] = Places["Name"]
        
        return self.quotes, self.airports
    
    def get_quotes_twoway(self, source, destination, outboundDate, inboundDate):
        """Gets the quotes for two specific dates. Only for roundway trips.
        Returns both 1) quotes in JSON format and 2) a dict of airport_code -> airport_name"""
        quoteRequestPath = "/apiservices/browsequotes/v1.0/"
        browseQuotesURL = self.rootURL + quoteRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/" + source + "/" + destination + "/" + outboundDate.strftime("%Y-%m-%d") + "/" + inboundDate.strftime("%Y-%m-%d")
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
        
        
    
    
