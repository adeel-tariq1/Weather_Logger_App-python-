
import openmeteo_requests
from openmeteo_requests import OpenMeteoRequestsError
import requests_cache
from retry_requests import retry
from city_coord import get_city
from database import (
    create_table,
    save_weather,
    get_history,
    get_cached_weather
)

forecast_url = "https://api.open-meteo.com/v1/forecast"

cache_session = requests_cache.CachedSession(
    ".cache", expire_after=3600
)
retry_session = retry(
    cache_session, retries=5, backoff_factor=0.2
)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather(city_name: str):
    cached = get_cached_weather(city_name)

    if cached is not None:
        return cached

    city = get_city(city_name)

    if not isinstance(city, dict):
        return city

    name = city["name"]
    country = city["country"]
    latitude = city["latitude"]
    longitude = city["longitude"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "relative_humidity_2m",
            "apparent_temperature",
            "weather_code"
        ]
    }

    try:
        responses = openmeteo.weather_api(
            forecast_url, params=params
        )
        response = responses[0]
        current = response.Current()

        temperature = current.Variables(0).Value()
        wind_speed = current.Variables(1).Value()
        humidity = current.Variables(2).Value()
        feels_like = current.Variables(3).Value()
        weather_code = int(current.Variables(4).Value())

        if weather_code == 0:
            condition = "☀️ Clear sky"
        elif weather_code == 1:
            condition = "🌤️ Mainly clear"
        elif weather_code == 2:
            condition = "⛅ Partly cloudy"
        elif weather_code == 3:
            condition = "☁️ Overcast"
        elif weather_code in (45, 48):
            condition = "🌫️ Fog"
        elif weather_code in (51, 53, 55):
            condition = "🌦️ Drizzle"
        elif weather_code in (56, 57):
            condition = "🧊 Freezing drizzle"
        elif weather_code in (61, 63, 65):
            condition = "🌧️ Rain"
        elif weather_code in (66, 67):
            condition = "🌧️ Freezing rain"
        elif weather_code in (71, 73, 75, 77):
            condition = "❄️ Snow"
        elif weather_code in (80, 81, 82):
            condition = "🌧️ Rain showers"
        elif weather_code in (85, 86):
            condition = "🌨️ Snow showers"
        elif weather_code in (95, 96, 99):
            condition = "⛈️ Thunderstorm"
        else:
            condition = "🌡️ Unknown weather condition"

        weather = {
            "city": name,
            "country": country,
            "temperature": round(temperature, 2),
            "wind_speed": round(wind_speed, 2),
            "weather_condition": condition,
            "feels_like": round(feels_like, 2),
            "humidity": round(humidity),
            "latitude": round(response.Latitude(), 2),
            "longitude": round(response.Longitude(), 2),
            "elevation": response.Elevation(),
        }

        save_weather(weather)
        return weather

    except OpenMeteoRequestsError as err:
        print(f"Debug error: {type(err).__name__}: {err}")
        return "Weather service is unavailable. Please try again."

    except Exception as err:
        print(f"Unexpected error: {type(err).__name__}: {err}")
        return "An unexpected error occurred."


if __name__ == "__main__":
    create_table()
    city_name = input("Enter city name: ").strip()
    weather = get_weather(city_name)
    print(weather)
