import os
import requests
from semantic_kernel.functions import kernel_function
import datetime

class WeatherPlugin:
    @kernel_function(name="get_weather", description="Get the current weather for a city")
    def get_weather(self, city: str, weatherdelta: int) -> str:
        """
        Retrieves the current weather for a specified city on the specified date.

        Args:
            city (str): The name of the city to get the weather for.
            weatherdelta (int): a number representing the number of hours from now to get the weather.

        Returns:
            str: A string describing the current weather and temperature in the specified city.
        """
        api_key = os.getenv("WEATHER_API_KEY")
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            target_date = datetime.datetime.now().date() + datetime.timedelta(hours=weatherdelta)
            weather_for_date = [
                item for item in data["list"]
                if datetime.datetime.fromtimestamp(item["dt"]).date() == target_date
            ]
            if weather_for_date:
                weather_description = weather_for_date[0]["weather"][0]["description"]
                temperature = weather_for_date[0]["main"]["temp"]
                return f"The weather in {city} on {target_date} is {weather_description} with a temperature of {temperature}°C."
            else:
                return f"Sorry, I couldn't retrieve the weather information for {city} on {target_date}."
        else:
            return "Sorry, I couldn't retrieve the weather information at the moment."
