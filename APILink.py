import geopy.exc, json, requests
from geopy import Nominatim

def get_api_data(url, apikey = None, params = ""):
    try:
        #this API uses dynamic URLs to sort data, so this way we have as many options as possible
        if apikey:
            headers =  {"User-Agent": apikey}
            response = requests.get(url + params, headers = headers, timeout=10)
        else:
            response = requests.get(url + params, timeout=10)
        return response
    except requests.exceptions.Timeout:
        print(f"Request timed out")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#despite the function name, this returns coordinates AND city name, to verify the returned location with the user
def get_coordinates(city, state) :
    #if the user somehow passes either nothing or an empty string, just terminate immediately without calling out
    if city is None or state is None or city == "" or state == "":
        print(f"Please select a city and state")
        return None, 35.159167, -98.442222
    else:
        try:
            location = Nominatim(user_agent="WeatherLightApp").geocode(f"{city}, {state}", country_codes="us", timeout=10)
            #Nominatim can find plenty more than cities, but cities will always be classified as boundaries or places
            #cities also tend to be the highest priority result when they exist, so we can still safely grab
            #just one result from Nominatim and be accurate as to if the location exists
            if location.raw.get("class") == "boundary" or location.raw.get("class") == "place":
                return location.address[:location.address.find(",")], location.latitude, location.longitude
            else: raise AttributeError("Result not a city or state")
        except AttributeError as e:
            print(f"An error occurred: {e}")
            print(f"No location found!")
            # if no location is found, default to Nowhere, OK's coordinates
            return None, 35.159167, -98.442222
        except geopy.exc.GeocoderTimedOut:
            print(f"Request timed out")
            # if no location is found, default to Nowhere, OK's coordinates
            return None, 35.159167, -98.442222
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"No location found!")
            # if no location is found, default to Nowhere, OK's coordinates
            return None, 35.159167, -98.442222

#uses user's IP address to roughly identify where they're located, to load the initial forecast
def get_user_location():
    try:
        location_data =  json.loads(requests.get("https://geolocation-db.com/json").text)
    except requests.exceptions.Timeout:
        print(f"Request timed out")
        # if no location is found, default to Nowhere, OK
        location_data = {"country_code": "US", "country_name": "United States", "city": "Nowhere", "postal": "73038",
                "latitude": 35.159167, "longitude": -98.442222, "IPv4": "0.0.0.0", "state": "Oklahoma"}
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Unable to determine current location")
        # if no location is found, default to Nowhere, OK
        location_data = {"country_code": "US", "country_name": "United States", "city": "Nowhere", "postal": "73038",
                "latitude": 35.159167, "longitude": -98.442222, "IPv4": "0.0.0.0", "state": "Oklahoma"}
    return location_data