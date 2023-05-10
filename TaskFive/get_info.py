import requests
from decouple import config


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
