import requests
from requests.exceptions import HTTPError,RequestException,ConnectionError,Timeout

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"

def get_city(city_name:str = None):
    if not city_name:
         city_name=input("Enter city name: ").strip()

    if not city_name:
         return "City name can not be empty."     
    url = GEO_URL
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    try:
        req = requests.get(url,params=params,timeout=5)
        req.raise_for_status()
        data = req.json()
        if data.get("results"):
                first_result = data["results"][0]
                return {
                    "name": first_result['name'],
                    "country":first_result['country'],
                    "latitude": first_result["latitude"],
                    "longitude": first_result["longitude"],
                }
        return "No city found. Kindly enter correct city name"
    except HTTPError as http_err:
        return f"Http Error occured {http_err},\n Status Code: {http_err.response.status_code}"
    except ConnectionError as errc:
               return (f"Connection Error (DNS failure, refused connection): {errc}")   
    except Timeout as errt:
               return (f"Timeout Error (Request timed out): {errt}")
    except RequestException as req_err:
        return f"A general Request exception occurred: {req_err}"
    


