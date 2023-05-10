from datetime import datetime

import requests
from decouple import config
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@db/{config("DB_NAME")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# migrate = Migrate(app, db)


class Weather:
    def __init__(self, city):
        self.city = city
        self.url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY')}&units=metric"

    def get_weather_info(self):
        while True:
            self.city = self.city.strip().replace(" ", "%20")

            if self.city.lower() == "stop":
                print("Exiting program.")
                exit(0)

            response = requests.post(self.url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error getting weather data for {self.city}.")


class WeatherModel(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Weather(city='{self.city}', temperature='{self.temperature}', humidity='{self.humidity}', description='{self.description}')"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/refresh_data", methods=["POST"])
def refresh_data():
    city = request.form["city"].capitalize()
    weather = WeatherModel.query.filter(WeatherModel.city == city).filter(
        db.func.DATE_PART("day", db.func.now() - WeatherModel.created_at) < 1
    ).order_by("created_at").first()
    if not weather:
        return jsonify({"error": "Weather data not available for the selected city from today."})
    result = {
        "city": weather.city,
        "temp": weather.temperature,
        "humidity": weather.humidity,
        "description": weather.description,
    }
    return jsonify(result)


@app.route("/get_data", methods=["POST"])
def get_data():
    city = request.form["city"].capitalize()
    weather = Weather(city)
    data = weather.get_weather_info()
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    # update weather data in the database
    existing_weather = WeatherModel.query.filter_by(city=city).first()
    if existing_weather:
        existing_weather.temperature = temp
        existing_weather.humidity = humidity
        existing_weather.description = description
        db.session.commit()
    else:
        new_weather = WeatherModel(city=city, temperature=temp, humidity=humidity, description=description)
        db.session.add(new_weather)
        db.session.commit()
    result = {
        "city": city,
        "temp": temp,
        "humidity": humidity,
        "description": description,
    }
    return jsonify(result)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
