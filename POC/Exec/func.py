import json
import urllib.request
import ssl
import random
import os
import sys
sys.path.append(os.getcwd())
import requests
import pytz
from datetime import datetime
import pygame
from Engine.DG import speak
from Assets.random import *
from Exec.phonebook import phone
from Exec.gears_info import gears
from Exec.image_gen import generate
from Exec.image_reocg import recog


ssl._create_default_https_context = ssl._create_unverified_context


pygame.mixer.init()

randomNews = random.choice(NewsUpdates)
randomWeather = random.choice(WeatherUpdates)
randomMusic = random.choice(MusicUpdates)
randomTime = random.choice(TimeUpdates)
randomDate = random.choice(DateUpdates)
randomDay = random.choice(DayUpdates)


def get_current_time_info(format_str, timezone='Asia/Karachi'):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz).strftime(format_str)
    return current_time

def get_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url)
        fact = response.json()['text']
        print(f"Fact of the day: {fact}")
        speak(f"Fact of the day: {fact}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fact: {e}")
 
def get_time():
    current_time = get_current_time_info('%I:%M %p')
    speak(f"{randomTime}{current_time}")

def get_date():
    current_date = get_current_time_info('%B %d, %Y')
    speak(f"{randomDate}{current_date}")

def get_day():
    current_day = get_current_time_info('%A')
    speak(f"{randomDay}{current_day}")

def get_news():
    country_code = "pk"
    num_headlines = 5
    api_key = "2b0508a5fc6577fbfbde3f53e0b4fd22"
    url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&country={country_code}&max={num_headlines}&apikey={api_key}"
    speak(randomNews)

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])
        if articles:
            for article in articles:
                title = article['title']
                print(f"Nemo: {title}")
                speak(title)
        else:
            print("No articles found.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")

def get_weather():
    url = 'https://wttr.in/lahore?format=%t+%C+%w'
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_info = response.text.strip().split()
        temperature = weather_info[0].split('°')[0]
        speak(f"{randomWeather}{temperature} centigrade")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")

def get_random_music():
    folder_path = 'Assets/Sounds/Music'
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        music_files = [f for f in files if f.endswith(('.mp3', '.wav'))]
        if not music_files:
            print("No music files found in the folder.")
            return
        music_file = random.choice(music_files)
        music_path = os.path.join(folder_path, music_file)
        print(f"Playing: {music_file}")
        speak(randomMusic)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing music: {e}")

def get_prayer_timings():
    try:
        date = datetime.now().strftime('%Y-%m-%d')

        def convert_to_12hr(time_str):
            return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p") if time_str else time_str

        url = f"http://api.aladhan.com/v1/timingsByAddress/{date}?address=Lahore"
        response = requests.get(url)
        response.raise_for_status()
        timings = response.json()['data']['timings']

        relevant_timings = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Sunset', 'Maghrib', 'Isha']
        print(f"Prayer Timings for Lahore on {date}:")
        for prayer in relevant_timings:
            if prayer in timings:
                print(f"{prayer}: {convert_to_12hr(timings[prayer])}")
                speak(f"{prayer}: {convert_to_12hr(timings[prayer])}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prayer timings: {e}")

def get_phone_number(query):
    resposne = phone(query)
    speak(resposne)
    print(resposne)

def get_gears_info(query):
    resposne = gears(query)
    speak(resposne)
    print(resposne)

def get_image_generation(query):
    resposne = generate(query)
    speak(resposne)
    print(resposne)

def get_image_recognition(query):
    resposne = recog(query)
    speak(resposne)
    print(resposne)


# if __name__ == "__main__":
#     print(get_phone_number("karimullah phone no"))

