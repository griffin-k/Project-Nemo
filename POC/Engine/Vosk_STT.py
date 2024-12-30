import sounddevice as sd
from vosk import Model, KaldiRecognizer
import queue
import json
import threading


def real_time_transcription(model_path: str):
    print("Loading Vosk model...")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)  

    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(f"Audio Input Status: {status}")
        audio_queue.put(bytes(indata))

    def process_audio():
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):  
                result = json.loads(recognizer.Result())
                print("You said:", result.get("text", ""))

    print("Starting microphone stream... Speak now!")

    # Start the transcription processing in a separate thread
    transcription_thread = threading.Thread(target=process_audio)
    transcription_thread.daemon = True  # Ensures the thread stops when the main program exits
    transcription_thread.start()

    # Start the microphone stream
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        try:
            while True:
                pass  # Main thread does nothing, as the audio processing is handled by the separate thread
        except KeyboardInterrupt:
            print("\nTranscription stopped.")


if __name__ == "__main__":
    vosk_model_path = "Assets/vosk-small"
    real_time_transcription(vosk_model_path)
