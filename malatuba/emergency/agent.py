#  agent.py
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from emergency.agents.ambulance_dispatch_agent import ambulance_dispatch_agent

# ---- Load environment variables ----
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
ROOT_AGENT_INSTR = """
- You are a travel concierge who also responds to emergencies.
- Use sub-agents like inspiration_agent or ambulance_dispatch_agent when applicable.
"""

root_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="root_agent",
    description="Main entry agent for travel and emergencies.",
    instruction=ROOT_AGENT_INSTR,
    sub_agents=[
        ambulance_dispatch_agent,
    ]
)
