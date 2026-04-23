import requests

def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]

        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]
        wind = current["windspeedKmph"]

        print(f"Weather in {city}:")
        print(f" Temprature: {temp_c}°C")
        print(f" Feels Like: {feels_like}°C")
        print(f" Humidity: {humidity}%")
        print(f" Wind Speed: {wind} km/h")
        print(f" Condition: {description}")

    except Exception as e:
        print(f"Could not get weather: {e}")

get_weather("Lahore")
print()
get_weather("Auckland")
print()
get_weather("London")
print()