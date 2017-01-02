from datetime import datetime
import functools
import os
from time import sleep

import requests
import serial

APPID = os.environ['OPENWEATHERMAP_API_KEY']


@functools.lru_cache(1)
def get_ip_location():
    return requests.get("http://freegeoip.net/json").json()


def get_weather(city=None, lat=None, lon=None):
    params = {"q": city, "lat": lat, "lon": lon, "appid": APPID}
    host = "http://api.openweathermap.org/data/2.5/weather"
    return requests.get(host, params=params).json()


def current_weather(city=None):
    if city:
        weather = get_weather(city=city)
    else:
        geo = get_ip_location()
        city = geo["city"]
        weather = get_weather(lat=geo["latitude"], lon=geo["longitude"])
    print_weather_to_lcd(city, weather)
    return weather


def print_lcd(text, port='/dev/ttyACM0', baudrate=9600):
    with serial.Serial(port=port, baudrate=baudrate) as ser:
        ser.write(str.encode(text))


def print_weather_to_lcd(city, weather):
    temp = kelvin_to_farenheit(weather["main"]["temp"])
    description = weather_description(weather)
    time_str = datetime.now().strftime("%a %I:%M%p, %d %b %Y")
    text = ("{time_str} | {city} | {temp}F | {desc}"
            .format(time_str=time_str, city=city, temp=temp, desc=description))
    print_lcd(text)


def weather_description(weather):
    descs = []
    for desc in weather["weather"]:
        descs.append(desc["description"])
    return " | ".join(descs)


def kelvin_to_farenheit(deg):
    return round((deg * 9/5) - 459.67)

def continuous_weather_updates(delay=120):
    current_weather()
    sleep(delay)

if __name__ == "__main__":
    continuous_weather_updates()
