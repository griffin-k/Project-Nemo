import subprocess
import tempfile
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

def speak(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        output_file = temp_file.name
 # Define voice options
        # voice = "en-US-JennyNeural"                    # Female
        # voice = "en-US-AriaNeural"                    # Female
        voice = "en-CA-ClaraNeural"                    # Female Speed
        # voice = "en-US-MichelleNeural"                 # Female good
        # voice = "en-IE-EmilyNeural"                     # Best female soft
        # voice = "en-US-AnaNeural"                      # Child
        # voice = "en-US-ChristopherNeural"              # Bold voice male
        # voice = "en-US-GuyNeural"                      # Male

        # voice = "en-CA-LiamNeural"  # Male Soft
      

        command = [
            'edge-tts',
            '--voice', voice,
            '--text', text,
            '--write-media', output_file
        ]

        try:
  
            subprocess.run(command, check=True, text=True, stderr=subprocess.PIPE)

    
            audio = AudioSegment.from_mp3(output_file)
            samples = np.array(audio.get_array_of_samples())
            sample_rate = audio.frame_rate
            sd.play(samples, samplerate=sample_rate)
            sd.wait()  
        
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")
        
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == '__main__':
    speak("Hello, how are you doing today. what is your name and what you can do for me ?")