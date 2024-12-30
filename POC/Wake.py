import sounddevice as sd
import pvporcupine
import numpy as np
import os

def callback(indata, frames, time, status):
    if status:
        print(f"Audio Input Status: {status}")
    audio_data = np.frombuffer(indata, dtype=np.int16)
    keyword_index = porcupine.process(audio_data)
    if keyword_index >= 0:
        print(f"Wake word detected! Keyword index: {keyword_index}")

def main():
    model_path = "nemo.ppn"
    access_key = "Okw7QOiFz0pf/H6iPBzar1vaqwxMumwQk6bB64BxqQX+B0ARfLsyTA=="
    global porcupine
    porcupine = pvporcupine.create(keyword_paths=[model_path], access_key=access_key)
    print("Listening for wake word...")
    with sd.RawInputStream(samplerate=16000, blocksize=512, dtype='int16', channels=1, callback=callback):
        while True:
            pass

if __name__ == "__main__":
    main()
