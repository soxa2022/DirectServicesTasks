from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .get_info import Weather
from .models import WeatherInfo


def index(request):
    return render(request, "index.html")


@csrf_exempt
def get_weather(request):
    if request.method == "POST":
        city = request.POST.get("city")
        weather_ = Weather(city)
        data = weather_.get_weather_info()
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        result = {
            "city": city[0].upper() + city[1:],
            "temp": temp,
            "humidity": humidity,
            "description": description[0].upper() + description[1:],
        }

        weather = WeatherInfo(
            city=result["city"],
            temperature=result["temp"],
            humidity=result["humidity"],
            description=result["description"],
        )
        weather.save()
        return JsonResponse(result)
    else:
        return render(request, "index.html")
