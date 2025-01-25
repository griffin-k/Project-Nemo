from groq import Groq
import os
import time
import sys
sys.path.append(os.getcwd())

from Engine.DG import speak

# from Engine.WebSTT import SpeechToTextListener
# listener = SpeechToTextListener(language="en-IN")
# listener.initialize_browser()



from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

custom_instructions = open(r'Prompts/persona/mera_bacha.txt').read().strip()

conversation_history = [
    {
        "role": "system",
        "content": custom_instructions
    },
    {
        "role": "system",
        "content": "Hello! How can I help you today?"
    }
]

def clean_response(response_text):
    cleaned_text = response_text.replace('*', '').strip()
    return cleaned_text

def chat(user_message, conversation_history=conversation_history, model="llama-3.1-70b-versatile", temperature=1, max_tokens=1024, top_p=1, stream=True, stop=None):
    client = Groq(api_key=GROQ_API_KEY)
    
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    completion = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=stream,
        stop=stop,
    )
    
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""
    
    response_text = clean_response(response_text)
    
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })
    
    return response_text


if __name__ == "__main__":
    while True:
        # user_message = listener.listen(prints=True)
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break
        response = chat(user_message)
        speak(response)
        # listener.reset_browser()
        # time.sleep(0.5)  
       
