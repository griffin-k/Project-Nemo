import json
import urllib.request
import ssl
import random
import os   
import sys
import requests
import pytz
from datetime import datetime
sys.path.append(os.getcwd())

from playsound import playsound
from Engine.DG import speak
from Assets.random import *


ssl._create_default_https_context = ssl._create_unverified_context

randonNews = random.choice(NewsUpdates)
randomWeather = random.choice(WeatherUpdates)
randomMusic = random.choice(MusicUpdates)
randomTime = random.choice(TimeUpdates)
randomDate = random.choice(DateUpdates)
randomDay = random.choice(DayUpdates)


def get_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    fact = response.json()['text']
    print(f"Fact of the day: {fact}")
    speak(f"Fact of the day: {fact}")

def get_time():
    pakistan_timezone = pytz.timezone('Asia/Karachi')
    pakistan_time = datetime.now(pakistan_timezone)
    final_time = pakistan_time.strftime('%I:%M %p')
    speak(f"{randomTime}{final_time}")  

def get_date():
    pakistan_timezone = pytz.timezone('Asia/Karachi')
    pakistan_date = datetime.now(pakistan_timezone)
    final_date = pakistan_date.strftime('%B %d, %Y')
    speak(f"{randomDate}{final_date}")  

def get_day():
    pakistan_timezone = pytz.timezone('Asia/Karachi')
    pakistan_date = datetime.now(pakistan_timezone)
    final_day = pakistan_date.strftime('%A')
    speak(f"{randomDay}{final_day}")  

def get_news():
    country_code = "pk"
    num_headlines = 5

    api_key = "2b0508a5fc6577fbfbde3f53e0b4fd22"
    url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&country={country_code}&max={num_headlines}&apikey={api_key}"
    speak(randonNews)
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            if "articles" in data:
                articles = data["articles"]
                for article in articles:
                    title = article['title']
                    print(f"Nemo : {title}")
                    speak(title)
            else:
                print("No articles found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_weather():
    url = 'https://wttr.in/lahore?format=%t+%C+%w'
    response = requests.get(url)
    response.raise_for_status()  
    weather_info = response.text.strip().split()
    temperature = weather_info[0].split('°')[0] 
    speak(f"{randomWeather}{temperature}centigrade")  

def get_random_music():
    folder_path = 'Assets/Sounds/Music'
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    music_files = [f for f in files if f.endswith(('.mp3', '.wav'))]
    if not music_files:
        print("No music files found in the folder.")
        return
    music_file = random.choice(music_files)
    music_path = os.path.join(folder_path, music_file)
    print(f"Playing: {music_file}")
    speak(randomMusic)
    playsound(music_path)




def get_prayer_timings():
    try:
        date = datetime.now().strftime('%Y-%m-%d')

        def convert_to_12hr(time_str): 
            return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p") if time_str else time_str

        url = f"http://api.aladhan.com/v1/timingsByAddress/{date}?address=Lahore"
        response = requests.get(url)
        response.raise_for_status()
        timings = response.json()['data']['timings']

        # Timings to include
        relevant_timings = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Sunset', 'Maghrib', 'Isha']

        print(f"Prayer Timings for Lahore on {date}:")
        for prayer in relevant_timings:
            if prayer in timings:
                print(f"{prayer}: {convert_to_12hr(timings[prayer])}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")






# if __name__ == "__main__":

