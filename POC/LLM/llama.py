from groq import Groq
import os
import sys
sys.path.append(os.getcwd())
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


custom_instructions = open(r'Prompts/about.txt').read().strip()


# Initialize the conversation history with the custom instructions
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



def chat(user_message, conversation_history=conversation_history, model="llama3-8b-8192", temperature=1, max_tokens=1024, top_p=1, stream=True, stop=None):
    client = Groq(api_key=GROQ_API_KEY)
    
    # Add the new user message to the conversation history
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
    
    # Add the model's response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": response_text
    })
    
    return response_text


# if __name__ == "__main__":
#     while True:
#         user_message = input("You: ")
#         if user_message.lower() == "exit":
#             break
#         response = chat(user_message)
#         print("Lune:", response)
#         print()
#         print("Conversation History:")
#         for message in conversation_history:
#             print(f"{message['role'].capitalize()}: {message['content']}")
#         print()

