import json, requests
from geopy import Nominatim

def get_api_data(url, apikey = None, params = ""):
    try:
        #this API uses dynamic URLs to sort data, so this way we have as many options as possible
        if apikey:
            headers =  {"User-Agent": apikey}
            response = requests.get(url + params, headers = headers)
        else:
            response = requests.get(url + params)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_coordinates(city, state) :
    try:
        location = Nominatim(user_agent="WeatherLightApp").geocode(f"{city}, {state}")
        return location.latitude, location.longitude
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Unable to determine current location")
        # if no location is found, default to Nowhere
        return 35.159167, -98.442222

def get_user_location():
    try:
        location_data =  json.loads(requests.get("https://geolocation-db.com/json").text)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Unable to determine current location")
        # if no location is found, default to Nowhere
        location_data = {"country_code": "US", "country_name": "United States", "city": "Nowhere", "postal": "73038",
                "latitude": 35.159167, "longitude": -98.442222, "IPv4": "0.0.0.0", "state": "Oklahoma"}
    return location_data