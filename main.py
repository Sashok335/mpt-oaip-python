import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_weather(city="Moscow"):

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 401:
            print("ОШИБКА (401): Неверный API-ключ. Проверьте config.py")
            return None
        elif response.status_code == 404:
            print(f"ОШИБКА (404): Город '{city}' не найден.")
            return None
        response.raise_for_status()

        data = response.json()

        weather_data = {
            "город": data.get("name"),
            "температура": data["main"].get("temp"),
            "описание": data["weather"][0].get("description") if data.get("weather") else "нет описания",
            "влажность": data["main"].get("humidity"),
            "ветер": data["wind"].get("speed")
        }
        return weather_data

    except requests.exceptions.Timeout:
        print("ОШИБКА:Таймаут")
    except requests.exceptions.RequestException as e:
        print("ОШИБКА:", e)


def main():
    city_need = "Moscow"
    print(f"Запрос погоды для: {city_need}")

    weather = get_weather(city=city_need)

    if not weather:
        print("Не удалось получить данные о погоде.")
        return

    print("\n--- Данные о погоде ---")
    print(f"Город: {weather['город']}")
    print(f"Температура: {weather['температура']}°C")
    print(f"Описание: {weather['описание']}")
    print(f"Влажность: {weather['влажность']}%")
    print(f"Скорость ветра: {weather['ветер']} м/с")


if __name__ == "__main__":
    main()