from groq import Groq
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import sys
from LLM.func import *
sys.path.append(os.getcwd())

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SystemPrompt = open(r'Prompts/about.txt').read().strip()

# Initialize Groq client
client = Groq()

# Model definitions
ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"


# Tool registry
TOOLS = {
    "music": play_random_music,
    "news":play_news,
    "weather":play_weather,

}


# Routing logic
def route_query(query):
    """Determine if a tool is needed for the query."""
    routing_prompt = f"""

    Given the following user query, determine if any tools are needed to answer it.

    If a time tool is needed, respond with 'TOOL: TIME'.
    If a music tool is needed, respond with 'TOOL: MUSIC'.
    If a news tool is needed, respond with 'TOOL: NEWS'.
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

# Tool handler
def run_with_tool(tool_name):
    """Execute the corresponding tool function based on the tool name."""
    tool_name = tool_name.split(":")[-1].strip().lower()
    if tool_name in TOOLS:
        return TOOLS[tool_name]()
    else:
        return json.dumps({"error": f"Tool '{tool_name}' not found."})
    
    

# General query handler
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

# Query processor
def process_query(query):
    """Process the query and decide whether to use tools or general model."""
    start_time = time.time()

    # Determine the route (tool or no tool)
    route = route_query(query)
    if "tool:" in route:
        response = run_with_tool(route)
    else:
        response = run_general(query)

    elapsed_time = time.time() - start_time

    return {
        "query": query,
        "route": route,
        "response": response,
        "time_taken": elapsed_time
    }

# Main execution
if __name__ == "__main__":
    queries = [
       "can you tell me the news update"
    ]

    for query in queries:
        result = process_query(query)
        print(f"Query: {result['query']}")
        print(f"Route: {result['route']}")
        print(f"Response: {result['response']}")
        print(f"Time Taken: {result['time_taken']} seconds\n")
