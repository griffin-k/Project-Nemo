import requests
from datetime import datetime

def get_prayer_timings_lahore():
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

get_prayer_timings_lahore()
