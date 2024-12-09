
import os
import requests
from semantic_kernel.functions import kernel_function

class WeatherPlugin:
    @kernel_function(name="get_weather", description="Get the current weather for a city")
    def get_weather(self, city: str) -> str:
        """
        Retrieves the current weather for a specified city.

        Args:
            city (str): The name of the city to get the weather for.

        Returns:
            str: A string describing the current weather and temperature in the specified city.
        """
        api_key = os.getenv("WEATHER_API_KEY")
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"The weather in {city} is currently {weather_description} with a temperature of {temperature}°C."
        else:
            return "Sorry, I couldn't retrieve the weather information at the moment."