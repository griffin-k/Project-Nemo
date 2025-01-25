import time
from Engine.WebSTT import SpeechToTextListener  
from LLM.llm_func import virtual_assistant  
from Engine.DG import speak 




def run_voice_assistant():
    print("Voice Assistant is ready. Say 'exit' to stop.")
    listener = SpeechToTextListener(language="en-US")
    listener.initialize_browser()

    while True:
        user_message = listener.listen(prints=True)
        if user_message.lower() == 'exit':  
            print("Exiting the voice assistant.")
            break
        Nemo_Response = virtual_assistant(user_message)
        print(f"Nemo: {Nemo_Response}")
        speak(Nemo_Response)  
        listener.reset_browser()
        time.sleep(0.5)  

if __name__ == "__main__":
    run_voice_assistant()