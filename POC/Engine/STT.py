import pygame
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class SpeechToTextListener:
    def __init__(
            self, 
            website_path: str = "https://realtime-stt-devs-do-code.netlify.app/", 
            language: str = "en-IN",  
            wait_time: int = 10,
            sound_file: str = "Assets/on.mp3"):  # Path to the MP3 file
        
        self.website_path = website_path
        self.language = language
        self.wait_time = wait_time
        self.sound_file = sound_file
        self.chrome_options = Options()
        self.chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.chrome_options.add_argument("--headless")  # Use standard headless mode for Raspberry Pi
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")  # GPU acceleration might not be supported on the Raspberry Pi
        self.driver = None 
        self.wait = None
        self.is_initialized = False
        self.recognized_text = ""

        # Initialize pygame for playing sound
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound_file)  # Load MP3 file for playback

    def initialize_browser(self):
        """Initialize the browser once."""
        if not self.is_initialized:
            driver_path = "/usr/bin/chromedriver"
            service = Service(driver_path)  
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.driver.get(self.website_path)
            self.wait.until(EC.presence_of_element_located((By.ID, "language_select")))
            self.select_language()  
            self.is_initialized = True
        else:
            print("Browser already initialized. Reusing the current session.")

    def play_start_sound(self):
        """Play the sound when listening starts."""
        pygame.mixer.music.play()

    def stream(self, content: str):
        """Display the user's speech text in real-time."""
        print("\033[96m\rUser Speaking: \033[93m" + f" {content}", end='', flush=True)

    def get_text(self) -> str:
        """Get the transcribed text from the browser."""
        return self.driver.find_element(By.ID, "convert_text").text

    def select_language(self):
        """Select the desired language for transcription (force English India)."""
        self.driver.execute_script(
            f"""
            var select = document.getElementById('language_select');
            select.value = '{self.language}';
            var event = new Event('change');
            select.dispatchEvent(event);
            """
        )
        # Ensure the language is selected after every transcription cycle.
        self.verify_language_selection()

    def verify_language_selection(self):
        """Verify if the correct language is selected."""
        language_select = self.driver.find_element(By.ID, "language_select")
        selected_language = language_select.find_element(By.CSS_SELECTOR, "option:checked").get_attribute("value")
        if selected_language != self.language:
            print(f"\033[91mLanguage mismatch: Expected {self.language}, found {selected_language}\033[0m")
            self.select_language()  # Force the selection again if the language is wrong

    def main(self) -> Optional[str]:
        """Main function to capture speech and return the transcription."""
        if not self.is_initialized:
            self.initialize_browser()

        self.select_language()  # Re-ensure correct language selection before starting transcription

        # Play the sound when starting to listen
        self.play_start_sound()

        self.driver.find_element(By.ID, "click_to_record").click()

        is_recording = self.wait.until(
            EC.presence_of_element_located((By.ID, "is_recording"))
        )

        print("\033[94m\rListening...", end='', flush=True)
        while is_recording.text.startswith("Recording: True"):
            text = self.get_text()
            if text:
                self.stream(text)
                self.recognized_text = text 
            is_recording = self.driver.find_element(By.ID, "is_recording")

        return self.recognized_text

    def listen(self, prints: bool = False) -> Optional[str]:
        """Listen for speech and return the transcribed text."""
        while True:
            result = self.main()
            if result and len(result) != 0:
                print("\r" + " " * (len(result) + 16) + "\r", end="", flush=True)
                if prints: print("\033[92m\rUser : " + f"{result}\033[0m\n")
                break
        return result

    def clear_text(self):
        """Clear the recognized speech text after sending it to LLM."""
        self.recognized_text = ""
        print("\033[91mTranscription data cleared.\033[0m")

    def reset_browser(self):
        """Reset the browser session and wait a short time to ensure the old text is cleared before the next cycle."""
        time.sleep(0.5)  
        self.driver.refresh()  
        self.clear_text()
