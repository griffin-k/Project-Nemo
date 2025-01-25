import requests
import random
import os 
import sys
sys.path.append(os.getcwd())
from Engine.streamTTS import speak

def fetch_random_hadith(api_key):
    url = "https://www.hadithapi.com/api/hadiths/"

    params = {
        "apiKey": api_key,
        "paginate": 100,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if response.status_code == 200:
            hadith_data = data.get("hadiths", {}).get("data", [])
            if isinstance(hadith_data, list) and hadith_data:
                random_hadith = random.choice(hadith_data)
                hadith_english = random_hadith.get('hadithEnglish', 'No English text available')

                return {"hadithEnglish": hadith_english.strip()}
            else:
                return {"error": "No Hadiths found in the response."}
        else:
            return {"error": data.get("message", "Unknown error occurred")}

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    API_KEY = "$2y$10$afpaGrCLtB7rXFSPRP3jmuExaZxLak7qLsoHx0XEH4IhsBBlSHW2u"

    result = fetch_random_hadith(api_key=API_KEY)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("Random Hadith:")
        print(f"English: {result['hadithEnglish']}")
        speak(result['hadithEnglish'])
