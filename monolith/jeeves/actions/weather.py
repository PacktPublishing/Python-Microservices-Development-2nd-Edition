import requests
from quart import current_app
from urllib.parse import quote as urlquote

# TODO aiohttp
# TODO wrapper for metrics recording.


def kelvin_to_celsius(kelvin):
    return int(kelvin - 273.15)


def process_weather_response(weather_data):
    # todo jinja template. render_template likely not suitable
    temperature = kelvin_to_celsius(weather_data["main"]["temp"])
    feels_like = kelvin_to_celsius(weather_data["main"]["feels_like"])
    return f"The temperature is {temperature}℃ and it feels like {feels_like}℃"

    dummy_response = {
        "coord": {"lon": 0.1167, "lat": 52.2},
        "weather": [
            {
                "id": 804,
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04n",
            }
        ],
        "base": "stations",
        "main": {
            "temp": 272.55,
            "feels_like": 270.05,
            "temp_min": 272.04,
            "temp_max": 273.15,
            "pressure": 1016,
            "humidity": 94,
        },
        "visibility": 10000,
        "wind": {"speed": 0.45, "deg": 273, "gust": 4.02},
        "clouds": {"all": 94},
        "dt": 1610056912,
        "sys": {
            "type": 3,
            "id": 39620,
            "country": "GB",
            "sunrise": 1610006808,
            "sunset": 1610035470,
        },
        "timezone": 0,
        "id": 2653941,
        "name": "Cambridge",
        "cod": 200,
    }


async def fetch_weather(location):
    text = urlquote(location)

    url = current_app.config["WEATHER_URL"].format(
        text=text, token=current_app.config["WEATHER_TOKEN"]
    )

    response = requests.get(url)
    response.raise_for_status()
    return process_weather_response(response.json())


async def weather_action(text, metadata):
    # Turn the text into something that's probably a location
    # Allow:
    # weather in location
    # weather location
    if not text:
        # TODO look up user.
        location = "London, UK"
    else:
        location = text.replace("weather", "").replace("in", "").strip()

    return await fetch_weather(location)
