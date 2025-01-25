from groq import Groq
import os
import sys
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

custom_instructions = open(r'Prompts/phonebook.txt').read().strip()


def phone(user_message, model="llama3-8b-8192", temperature=1, max_tokens=1024, top_p=1, stream=True, stop=None):
    client = Groq(api_key=GROQ_API_KEY)
    

    conversation_history = [
        {
            "role": "system",
            "content": custom_instructions
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
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
    
    return response_text


