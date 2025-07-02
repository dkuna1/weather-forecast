from flask import Flask, render_template, request
from configparser import ConfigParser
from urllib import request as urlrequest, parse
import json

app = Flask(__name__)
API_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def build_url(city, api_key):
    query = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    return f"{API_URL}?{parse.urlencode(query)}"

def get_weather(city):
    try:
        api_key = get_api_key()
        url = build_url(city, api_key)
        response = urlrequest.urlopen(url)
        data = json.loads(response.read())
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather = get_weather(city)
            if not weather:
                error = "City not found or API error."
    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
