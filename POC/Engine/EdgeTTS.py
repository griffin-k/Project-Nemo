import subprocess
import tempfile
import os
import pygame
from pydub import AudioSegment


# person = "en-CA-ClaraNeural" 

# voice = "ur-PK-OmarNeural"
# voice = "en-US-JennyNeural"                    # Female
# voice = "en-US-AriaNeural"                    # Female
# person = "en-CA-ClaraNeural"                    # Female Speed
# voice = "en-US-MichelleNeural"                 # Female good
# voice = "en-IE-EmilyNeural"                     # Best female soft
# voice = "en-US-AnaNeural"                      # Child
# voice = "en-US-ChristopherNeural"              # Bold voice male
# voice = "en-US-GuyNeural"                      # Male
# voice = "en-CA-LiamNeural"  # Male Soft


# Hindi voices
# person ="hi-IN-MadhurNeural"
person = "hi-IN-SwaraNeural"




def speak(text, voice=person):
    try:
        pygame.mixer.init()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            output_file = temp_file.name

            command = [
                'edge-tts',
                '--voice', voice,
                '--text', text,
                '--write-media', output_file
            ]

            subprocess.run(command, check=True, text=True, stderr=subprocess.PIPE)

            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            os.remove(output_file)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# if __name__ == '__main__':
#     speak("kia hal hai")