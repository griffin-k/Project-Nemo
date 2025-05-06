import requests
import os
from typing import Union
import sys
import time
import threading
from colorama import Fore, init
import base64
import pygame

def generate_audio(message: str, model: str = "aura-asteria-en") -> Union[None, bytes]:
    url = "https://deepgram.com/api/ttsAudioGeneration"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    payload = {"text": message, "model": model}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()

        if 'data' in response_json:
            return base64.b64decode(response_json['data'])
        else:
            print(f"Error: 'data' key not found in response: {response_json}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def print_animated_message(message):
    prefixed_message = f"Nemo -> {message}"  
    for char in prefixed_message:
        sys.stdout.write(Fore.GREEN + char)
        sys.stdout.flush()
        time.sleep(0.050) 
    print(Fore.RESET)  

def save_audio(audio_content: bytes, folder: str = "", filename: str = "output.mp3") -> Union[None, str]:
    if not audio_content:
        print("No audio content to save.")
        return None

    try:
        file_path = os.path.join(folder, filename)
        with open(file_path, 'wb') as audio_file:
            audio_file.write(audio_content)
        return file_path
    except Exception as e:
        print(f"Error saving audio to file: {e}")
        return None

def Co_speak(message: str, voice: str = "aura-stella-en", folder: str = "", extension: str = ".mp3") -> Union[None, str]:
    try:
        result_content = generate_audio(message, voice)
        if result_content is None:
            return None

        file_path = save_audio(result_content, folder, f"{voice}{extension}")
        if file_path:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            os.remove(file_path)
        return None
    except Exception as e:
        print(e)

def speak(text: str):
    t1 = threading.Thread(target=Co_speak, args=(text,))
    t2 = threading.Thread(target=print_animated_message, args=(text,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

# if __name__ == "__main__":
