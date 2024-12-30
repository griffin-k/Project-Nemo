import requests 
from playsound import playsound 
import os
from typing import Union 
import sys
import time
import threading
from colorama import Fore, init

def generate_audio(message: str, voice: str = "en-US-Wavenet-C"):
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"

    headers = {'User-Agent':'Mozilla/5.0(Maciontosh;intel Mac OS X 10_15_7)AppleWebKit/537.36(KHTML,like Gecoko)Chrome/119.0.0.0 Safari/537.36'}
    
    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except:
        return None
    
def print_animated_message(message):
    prefixed_message = f"Nemo -> {message}"  
    for char in prefixed_message:
        sys.stdout.write(Fore.GREEN + char)  # Color text green
        sys.stdout.flush()
        time.sleep(0.050) 
    print(Fore.RESET)  

# Kimberly

# en-US-Wavenet-F
# en-US-Wavenet-D

def Co_speak(message: str, voice: str = "en-US-Wavenet-D", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        with open(file_path, "wb") as file:
            file.write(result_content)
        playsound(file_path)
        os.remove(file_path)
        return None
    except Exception as e:
        print(e)

def speak(text):
    t1 = threading.Thread(target=Co_speak, args=(text,))
    t2 = threading.Thread(target=print_animated_message, args=(text,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


# if __name__ == "__main__":
#     speak("Hello, I am Nemo. How can I help you?")
