from google.adk.agents import Agent
from .prompt import ROOT_AGENT_INSTRUCTION
from google.adk.tools.google_search_tool import google_search
from .search import Hospital_Search_Agent as Search_Agent_Grounding
from .call_agent import call_agent_tool as Call_Agent_Tool
from .gps_location import GetCurrentLocationTool

AGENT_MODEL = "gemini-2.5-flash-preview-05-20"

root_agent = Agent(
    name = "Ambulance Agent",
    model = AGENT_MODEL,
    description=("""
        You are an AI agent designed to assist users in an emergency situation by doing the following:
        1. Identifying and verifying the emergency situation.
        2. Pinpointing the user's exact location using GPS coordinates.
        3. Searching for the nearest hospital or medical facility using the user's location.
        4. Contacting the ambulance service to dispatch an ambulance to the user's location.
        """
    ),
    instruction = ROOT_AGENT_INSTRUCTION,
    tools = [Search_Agent_Grounding, Call_Agent_Tool, GetCurrentLocationTool],
)