import subprocess
import os
import pygame

# Voice selection (adjust as needed)
person = "en-CA-LiamNeural"  # Male Soft Voice


# Output file path
output_file = "message_audio.mp3"

def generate_audio(text, voice=person, output=output_file):
    try:
        # Generate speech using edge-tts
        command = [
            'edge-tts',
            '--voice', voice,
            '--text', text,
            '--write-media', output
        ]
        subprocess.run(command, check=True, text=True, stderr=subprocess.PIPE)
        print(f"Audio saved as: {output}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def play_audio(file):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")

# if __name__ == '__main__':
#     generate_audio("You are looking down, please look forward.")
#     play_audio(output_file)  # Play after generating
