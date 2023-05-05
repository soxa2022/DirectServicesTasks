from flask import Flask, render_template, request, jsonify

from get_info import Weather

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def get_weather():
    city = request.form["city"]
    weather = Weather(city)
    data = weather.get_weather_info()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    result = {
        "city": city[0].upper() + city[1:],
        "temp": temp,
        "humidity": humidity,
        "description": description[0].upper() + description[1:],
    }
    return render_template("index.html", **result)


if __name__ == "__main__":
    app.run(debug=True)
