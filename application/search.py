# -*- coding: utf-8 -*-
import json
import requests
import datetime
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
    
    def __init__(self, originCountry = "US", currency = "USD", locale = "en-US"):
        """Creates a SkyScanner object with default country, currency, and local
        which can be changed as necessary. In addition, a requests session is made."""
        self.originCountry = originCountry
        self.currency = currency
        self.local = locale
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
        browsePlacesURL = self.rootURL + self.placeRequestPath + self.originCountry + "/" + self.currency + "/" + self.locale + "/"
        response = self.session.get(browsePlacesURL, params=params)
        resultJSON = json.loads(response.text)
        return resultJSON
    
    
        
        
    
    
