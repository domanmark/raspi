import requests
import json
import sys
import time
import random
from flask import Flask, render_template

# read in private configurations file
try:
    with open('api_config.json', 'r') as f:
        keys = json.load(f)
except FileNotFoundError:
    print('API config file not found. Please provide api_config.json')
    sys.exit(1)

# get private information from config file
DARK_SKY_KEY = keys['DARK_SKY_KEY']
GOOGLE_MAPS_KEY = keys['GOOGLE_MAPS_KEY']
BING_MAPS_KEY = keys['BING_MAPS_KEY']
DIRECTION_WAYPOINTS = keys['DIRECTION_WAYPOINTS']
LAT = keys['LATITUDE']
LONG = keys['LONGITUDE']
NEWS_API_KEY = keys['NEWS_API_KEY']

app = Flask(__name__)

@app.route("/news")
def news():
    news = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey={}".format(
        NEWS_API_KEY
        )
    )
    news_json = json.loads(news.text)
    headlines = []
    for article in news_json["articles"]:
        headlines.append(article["title"])
    random_headlines = random.sample(headlines, 3)
    return '<br><br>'.join(random_headlines)

@app.route("/weather")
def weather():
    weather = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(
        DARK_SKY_KEY,
        LAT,
        LONG
        )
    )
    weather_json = json.loads(weather.text)

    return (time.ctime()
            + "<br></br>Current weather: "
            + str(weather_json["currently"]["temperature"])
            + "&#176;"
            + " and "
            + str(weather_json["currently"]["summary"])
            + "<br></br>Forecast: "
            + str(weather_json["hourly"]["summary"])
            )

@app.route("/directions")
def directions():
    origin = DIRECTION_WAYPOINTS['origin']
    destination = DIRECTION_WAYPOINTS['destination']
    midpoint = DIRECTION_WAYPOINTS['midpoint']
    directions = requests.get("http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0={}%2Cwa&wp.1={}%2Cwa&wp.2={}%2Cwa&&key={}&optmz=timeWithTraffic".format(
        origin,
        midpoint,
        destination,
        BING_MAPS_KEY
        )
    )
    directions_json = json.loads(directions.text)
    drive_time = directions_json['resourceSets'][0]['resources'][0]['travelDurationTraffic'] / 60 # time in mins

    return "Time to work: {:.2f} mins".format(drive_time)

@app.route("/dashboard")
def dashboard():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()