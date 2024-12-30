from groq import Groq
import os
import time
from dotenv import load_dotenv
import sys
sys.path.append(os.getcwd())

from LLM.func import *  

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SystemPrompt = open(r'Prompts/about.txt').read().strip()

client = Groq()

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

# Define tools available for use
TOOLS = {
    "fact": get_fact,
    "time": get_time,
    "date": get_date,
    "day": get_day,
    "news": get_news,
    "music": get_random_music,
    "weather": get_weather,
  
}

def virtual_assistant(query):
  
    def route_query(query):
   
        routing_prompt = f"""
        Given the following user query, determine if any tools are needed to answer it.
        
        If a fact tool is needed, respond with 'TOOL: FACT'.
        If a time tool is needed, respond with 'TOOL: TIME'.
        If a date tool is needed, respond with 'TOOL: DATE'.
        If a day tool is needed, respond with 'TOOL: DAY'.
        If a fact tool is needed, respond with 'TOOL: FACT'.
        If a news tool is needed, respond with 'TOOL: NEWS'.
        If a music tool is needed, respond with 'TOOL: MUSIC'.
        If a weather tool is needed, respond with 'TOOL: WEATHER'.

       
        If no tools are needed, respond with 'NO TOOL'.
        User query: {query}
        Response:
        """
        response = client.chat.completions.create(
            model=ROUTING_MODEL,
            messages=[
                {"role": "system", "content": "You are a routing assistant. Determine if tools are needed based on the user query."},
                {"role": "user", "content": routing_prompt}
            ],
            max_tokens=20
        )
        return response.choices[0].message.content.strip().lower()

   
    def run_with_tool(tool_name):
        """Execute the corresponding tool function based on the tool name."""
        tool_name = tool_name.split(":")[-1].strip().lower()
        if tool_name in TOOLS:
            return TOOLS[tool_name]()
        else:
            return f"Error: Tool '{tool_name}' not found."  


    def run_general(query):
        """Answer the query using the general model."""
        response = client.chat.completions.create(
            model=GENERAL_MODEL,
            messages=[
                {"role": "system", "content": SystemPrompt},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content

 
    def process_query(query):
        """Process the query and return the appropriate response."""
        # Determine the route (tool or no tool)
        route = route_query(query)
        if "tool:" in route:
            return run_with_tool(route) 
        else:
            return run_general(query)  


    response = process_query(query)
    return response  

# # Example usage
# if __name__ == "__main__":
#     query = "what is the weather update?"
#     response = virtual_assistant(query)
#     print(f"Response: {response}")  # Just print the final response
