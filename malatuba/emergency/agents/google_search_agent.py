# google_search_agent

from google.adk.agents import Agent
from google.adk.tools import google_search
from emergency.services.places_service import PlacesService



google_search_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="google_search_agent",
    description="Searches the web for nearby hospitals and relevant info.",
    instruction="Use this agent to search the web. Return hospital names from search results.",
    tools=[google_search],
)
