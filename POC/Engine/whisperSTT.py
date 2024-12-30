import os
from colorama import Fore
import sounddevice as sd
import io
from scipy.io.wavfile import write
from groq import Groq
from dotenv import load_dotenv
import threading
from playsound import playsound  

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def play_sound(sound_file):
    playsound(sound_file)  # Use playsound to play the sound file

def listen(duration=5, samplerate=44100):
    try:
        print("Start Listening...")
        sound_thread = threading.Thread(target=play_sound, args=("Assets/on.mp3",))
        sound_thread.start()
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
        sd.wait()  

        sound_thread.join()  

        byte_io = io.BytesIO()
        write(byte_io, samplerate, audio_data)
        byte_io.seek(0)

        transcription = client.audio.transcriptions.create(
            file=("recorded_audio.wav", byte_io.read()),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="verbose_json",
        )

        print("Transcription Complete")
        print(Fore.WHITE +"User -> "+ transcription.text + Fore.RESET)

        return transcription.text

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Recording Started..")
    transcribed_text = listen()
    if transcribed_text:
        print("Transcribed Text:")
        print(transcribed_text)
