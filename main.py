import json
from configparser import ConfigParser
from urllib import request, parse, error

API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def build_url(city, api_key, imperial=False):
    query = {
        "q": city,
        "appid": api_key,
        "units": "imperial" if imperial else "metric",
    }
    return f"{API_URL}?{parse.urlencode(query)}"

def get_weather_data(url):
    try:
        response = request.urlopen(url)
        data = response.read()
        return json.loads(data)
    except error.HTTPError as http_err:
        if http_err.code == 404:
            print("City not found.")
        else:
            print(f"HTTP Error: {http_err.code}")
        return None

def display_weather_info(weather_data, imperial=False):
    if weather_data:
        city = weather_data["name"]
        description = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        unit = "F" if imperial else "C"
        print(f"{city:>20}\t{description:>20} ({temp}°{unit})")

def main():
    city = input("Enter a city name: ").strip()
    unit_input = input("Use imperial units (F)? Type 'yes' or press Enter for metric (C): ").lower()
    imperial = unit_input == "yes"

    api_key = get_api_key()
    url = build_url(city, api_key, imperial)
    weather_data = get_weather_data(url)
    display_weather_info(weather_data, imperial)

if __name__ == "__main__":
    main()
