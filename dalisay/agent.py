from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

from .sub_agents.emergency_operator import emergency_operator_agent
from .sub_agents.gps_locator import gps_locator_agent
from .sub_agents.web_searcher import web_searcher_agent

MODEL = 'gemini-2.0-flash-exp'

root_agent = Agent(
  name='iloilo_province_ambulance_support_agent',
  model=MODEL,
  instruction=prompt.AMBULANCE_SUPPORT_PROMPT,
  description='To provide ambulance support to the user by identifying and verifying the stated emergency, pinpointing their exact location and using it to search for a nearby hospital, and contacting the ambulance service.',
  tools=[
    AgentTool(agent=web_searcher_agent),
    AgentTool(agent=gps_locator_agent),
    AgentTool(agent=emergency_operator_agent)
  ],
)

