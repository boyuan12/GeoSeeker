import os
from flask import Flask, render_template
import requests
import json
import random

app = Flask(__name__)

elk_grove = requests.get("https://storage.googleapis.com/geoseekeraddress/us_ca_city_of_elk_grove-addresses-city.geojson")
elk_grove = elk_grove.text
elk_grove = elk_grove.split("\n")

# nyc = requests.get("https://storage.googleapis.com/geoseekeraddress/us_ny_city_of_new_york-addresses-city.geojson")
# nyc = nyc.text
# nyc = nyc.split("\n")

# utah = requests.get("https://storage.googleapis.com/geoseekeraddress/statewide-addresses-state.geojson")
# utah = utah.text
# utah = utah.split("\n")

total_address = elk_grove # + nyc + utah

@app.route('/')
def index():
  parsed = json.loads(random.choice(total_address))
  lng = parsed["geometry"]["coordinates"][0]
  lat = parsed["geometry"]["coordinates"][1]
  get_nearest_road_coord(lat, lng)
  return render_template("index.html", lat=lat, lng=lng)

def get_nearest_road_coord(lat, lng):
  url = f"https://roads.googleapis.com/v1/nearestRoads?points={lat},{lng}&key=AIzaSyCTp9yLnUVpd2pEyAmRx5e2kkybGaO3AOQ"
  
  payload={}
  headers = {}
  
  response = requests.request("GET", url, headers=headers, data=payload)
  
  print(response.json())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
