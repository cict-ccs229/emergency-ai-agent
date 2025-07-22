from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

search_agent = Agent (
    name="Hospital Search Agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Agent to search for nearby hospitals within the user's given location and return detailed information."
    ),
    instruction=("""
    You are an AI agent designed to search for hospitals in the user's area. 
    When the user provides their location, you will use the Google Search tool to find the nearest hospitals
    Use the provide coordinates or location to search for hospitals.
    If the user does not provide a specific location, you will use their IP address to determine their current location.
    """
    ),
    tools=[google_search],
)

Hospital_Search_Agent = AgentTool(agent=search_agent)
