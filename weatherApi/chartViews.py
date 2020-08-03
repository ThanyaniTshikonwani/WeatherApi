import requests

from django.shortcuts import render

from .config.remote import getUrl, getOneCallUrl
from .config.timestamp import get_Date
from .forms import Post


def chart(request):
    def post():
        post = "Johannesburg"

        if request.method == "POST":
            form = Post(request.POST)

            if form.is_valid():
                post = form.cleaned_data.get('post')

        get_weather = getUrl("weather", "metric") + post
        return get_weather

    response = requests.get(post())

    def get_weatherCoords():
        getCoord = response.json()

        lon = getCoord["coord"]["lon"]
        lat = getCoord["coord"]["lat"]

        get_daily_weather = getOneCallUrl(str(lat), str(lon))
        get_daily_weather_response = requests.get(get_daily_weather)

        return get_daily_weather_response

    if get_weatherCoords().status_code == 200:
        get_daily_weather_response_data = get_weatherCoords().json()
        get_daily_weather_response_list = get_daily_weather_response_data["daily"]

        daily_forecast = []
        for i in range(0, 7):
            timestamp = get_daily_weather_response_list[i]["dt"]

            date = get_Date(timestamp)

            day_temp = int(get_daily_weather_response_list[i]["temp"]["day"])
            day_eve = int(get_daily_weather_response_list[i]["temp"]["eve"])
            day_morn = int(get_daily_weather_response_list[i]["temp"]["morn"])
            day_night = int(get_daily_weather_response_list[i]["temp"]["night"])
            temp_median = int((day_temp + day_eve + day_morn + day_night) / 4)

            day_temp_min = (get_daily_weather_response_list[i]["temp"]["min"])
            day_temp_max = int(get_daily_weather_response_list[i]["temp"]["max"])
            avg_temp = int((day_temp_min + day_temp_max) / 2)

            daily_data = [
                # "Date": date,
                day_temp_min
                # "High": day_temp_max,
                # "humidity": get_daily_weather_response_list[i]["humidity"],
                # "Temp_median": temp_median,
                # "Avg_temp": avg_temp,
                # "description": get_daily_weather_response_list[i]["weather"][0]["description"],
                # "icon": get_daily_weather_response_list[i]["weather"][0]["icon"],
            ]
            daily_forecast.append(daily_data)



    else:
        daily_forecast = {}

    return render(request, 'views/index.html', )