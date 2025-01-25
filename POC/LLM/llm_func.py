from groq import Groq
import os
import time
from dotenv import load_dotenv
import sys
sys.path.append(os.getcwd())

from Exec.func import *  
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SystemPrompt = open(r'Prompts/about.txt').read().strip()

client = Groq()

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama-3.3-70b-versatile"
GENERAL_MODEL = "llama-3.3-70b-versatile"

TOOLS = {
    "fact": get_fact,
    "time": get_time,
    "date": get_date,
    "day": get_day,
    "news": get_news,
    "music": get_random_music,
    "weather": get_weather,
    "phone": get_phone_number,
    "gears": get_gears_info,
    "pryer": get_prayer_timings,
}


conversation_context = [{"role": "system", "content": SystemPrompt}]

def virtual_assistant(query):
    def route_query(query):
        routing_prompt = f"""
        Given the following user query, determine if any tools are needed to answer it.
        If the query requires only fact of the Day, respond with 'TOOL: FACT'.
        If the query involves checking the current time, respond with 'TOOL: TIME'.
        If the query involves today's date, respond with 'TOOL: DATE'.
        If the query is about the day of the week, respond with 'TOOL: DAY'.
        If the query involves recent news, respond with 'TOOL: NEWS'.
        If the query asks for music recommendations, respond with 'TOOL: MUSIC'.
        If the query involves weather updates, respond with 'TOOL: WEATHER'.
        If the user is seeking a service phone number, respond with 'TOOL: PHONE'.
        If the query is related to Garrison Engineering & Robotics Society (GEARS) data, respond with 'TOOL: GEARS'.
        If the query is about prayer timings, respond with 'TOOL: PRYER'.
        If no tools are needed, respond with 'NO TOOL'.
        User query: {query}
        Response:

        """
        response = client.chat.completions.create(
            model=ROUTING_MODEL,
            messages=[
                {"role": "system", "content": "You are a routing assistant. Determine if tools are needed based on the user query carefully."},
                {"role": "user", "content": routing_prompt}
            ],
            max_tokens=20
        )
        return response.choices[0].message.content.strip().lower()

    def run_with_tool(tool_name, query):
        """Execute the corresponding tool function based on the tool name."""
        tool_name = tool_name.split(":")[-1].strip().lower()
        if tool_name in TOOLS:
            if tool_name == "phone":
                return TOOLS[tool_name](query)
            elif tool_name == "gears":
                return TOOLS[tool_name](query)
            else:
                return TOOLS[tool_name]()
        else:
            return f"Error: Tool '{tool_name}' not found."

    def run_general(query):
        """Answer the query using the general model."""
        global conversation_context
        conversation_context.append({"role": "user", "content": query})
        response = client.chat.completions.create(
            model=GENERAL_MODEL,
            messages=conversation_context
        )
        # Add the assistant's response to the conversation context
        assistant_response = response.choices[0].message.content
        conversation_context.append({"role": "assistant", "content": assistant_response})
        return assistant_response

    def process_query(query):
        """Process the query and return the appropriate response.""" 
        route = route_query(query)
        if "tool:" in route:
            return run_with_tool(route, query) 
        else:
            return run_general(query)

    response = process_query(query)
    return response


if __name__ == "__main__":
    while True:
        query = input("Enter a query: ")
        response = virtual_assistant(query)
        print(f"Response: {response}")
