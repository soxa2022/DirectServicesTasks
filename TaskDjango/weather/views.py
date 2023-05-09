from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from weather.models import WeatherInfo
from .get_info import Weather


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


@csrf_exempt
def get_data(request):
    if request.method == "POST":
        city = request.POST.get("city")
        data = WeatherInfo.objects.filter(city__iexact=city).order_by("created_at")[:10]
        if data:
            coldest = min(data, key=lambda x: x.temperature)
            created_at = coldest.created_at.strftime('%Y-%m-%d %H:%M')
            temp = coldest.temperature
            humidity = coldest.humidity
            result = {
                "city": city[0].upper() + city[1:],
                "temp": temp,
                "humidity": humidity,
                "description": created_at,
            }

            return JsonResponse(result)
    else:
        return render(request, "index.html")
