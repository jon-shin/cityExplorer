from os import name
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import requests, json
from pytz import timezone
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import flag


app = Flask(__name__)
geolocator = Nominatim(user_agent="my-project")
tf = TimezoneFinder()
api_key = "d5c59fc08da49a070c3380f83f3e05b3"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
      city = request.form['city']
      now_utc = datetime.now(timezone('UTC'))
      complete_url = base_url + "appid=" + api_key + "&q=" + city
      response = requests.get(complete_url)
      x = response.json()
      if x["cod"] != "404":
        y = x["main"]
        kelvin = y["temp"]
        temp = round((kelvin - 273.15) * 9/5 + 32, 2)
        z = x["weather"]
        desc = z[0]["description"]
        pressure = y["pressure"]
        humidity = y["humidity"]
        location = geolocator.geocode(city)
        lat = location.latitude
        long = location.longitude
        rev = geolocator.reverse(str(lat)+","+str(long))
        address = rev.raw['address']
        country = country = address.get('country', '')
        code = address.get('country_code')
        f = flag.flagize(":"+str(code)+":")
        tz = tf.timezone_at(lng = long, lat = lat) 
        current_time = now_utc.astimezone(timezone(tz))
        date = current_time.strftime('%Y-%m-%d')
        time = current_time.strftime('%H:%M')
        return render_template("prj2.html", country = country, flag = f, date = date, city = city, time = time, 
        temp = temp, desc=desc, lat = lat, long = long, pressure = pressure, humidity = humidity)
      else:
        return redirect(url_for('not_found'))
    else:
      return render_template("prj2.html")
    
@app.route("/not_found", methods = ['POST', 'GET'])
def not_found():
  return render_template("not_found.html")

if __name__ == "__main__":
    app.run(debug = True)



