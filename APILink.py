import json, requests
from StateAbbreviationDict import state_abbreviations
import sys


def get_api_data(url, apikey = None, params = ""):
    try:
        if apikey:
            headers =  {"User-Agent": apikey}
            response = requests.get(url + params, headers = headers)
        else:
            response = requests.get(url + params)
        #this API uses dynamic URLs to sort data, so this way we have as many options as possible
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_location(address):
    try:
        modified_address = address
        modified_address = modified_address.replace(" ", "+").replace(",", "%2C").replace(".", "")
        address_data =  json.loads(requests.get(
            "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" +
            modified_address + "&benchmark=4&format=json").text)
        temp_city = address_data["result"]["addressMatches"][0]["addressComponents"]["city"]
        temp_city = temp_city[:1] + temp_city[1:].lower()
        if not temp_city in modified_address or not address_data["result"]["addressMatches"][0]["addressComponents"]["state"] in modified_address:
            raise Exception("No valid address found!")
        location_data = {"country_code": "US", "country_name": "United States",
                         "city": temp_city,
                         "postal": address_data["result"]["addressMatches"][0]["addressComponents"]["zip"],
                         "latitude": address_data["result"]["addressMatches"][0]["coordinates"]["y"],
                         "longitude": address_data["result"]["addressMatches"][0]["coordinates"]["x"],
                         "IPv4": "0.0.0.0",
                         "state": state_abbreviations[address_data["result"]["addressMatches"][0]["addressComponents"]["state"]]}
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Unable to determine current location")
        location_data = {"country_code": "US", "country_name": "United States", "city": "Nowhere", "postal": "73038",
                "latitude": 35.159167, "longitude": -98.442222, "IPv4": "0.0.0.0", "state": "Oklahoma"}
        #if no location is found, default to nowhere
    return location_data

def get_user_location():
    try:
        location_data =  json.loads(requests.get("https://geolocation-db.com/json").text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Unable to determine current location")
        location_data = {"country_code": "US", "country_name": "United States", "city": "Nowhere", "postal": "73038",
                "latitude": 35.159167, "longitude": -98.442222, "IPv4": "0.0.0.0", "state": "Oklahoma"}
        #if no location is found, default to nowhere
    return location_data