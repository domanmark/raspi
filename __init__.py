import requests
import json
import sys
import time
from flask import Flask, render_template

# get DarkSky API key stored outside the app source code
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

app = Flask(__name__)

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
            + "<br></br>Current temp: "
            + str(weather_json["currently"]["temperature"])
            + "&#176;"
            + "<br></br>Today's forecast: "
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
    return "time to work: {:.2f} mins".format(drive_time)

@app.route("/dashboard")
def dashboard():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()