import random

import geocoder
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from . import prompt

def get_current_location_tool(location: str) -> dict:
  g = geocoder.google(location)

  if g.ok:
    # Check if the location is within Iloilo Province
    # if g.city == 'Iloilo' and g.country == 'Philippines':
      return { 'status': 'success', 'report': (f'Your current location is {g.address} with a lattitude and longitude of {g.latlng}.') }
  else:
    return { 'status': 'error', 'report': 'Service not available in your location. Please provide a location within Iloilo Province.' }

def contact_ambulance_tool() -> str:
  return 'Ambulance service contacted successfully', 200 if random.random() > 0.5 else 'Failed to contact ambulance service', 500

google_search_agent = Agent(
  name='google_search_tool',
  model='gemini-2.0-flash',
  instruction='Search for the nearest hospital and contact the ambulance service.',
  description='Search for the nearest hospital and contact the ambulance service using Google Search.',
  tools=[
    google_search
  ]
)

gps_location_agent = Agent(
  name='get_current_location_tool',
  model='gemini-2.0-flash',
  instruction='Get the current location of the user.',
  description='Get the current location of the user using geocoder.',
  tools=[
    get_current_location_tool
  ]
)

contact_ambulance_agent = Agent(
  name='get_current_location_tool',
  model='gemini-2.0-flash',
  instruction='Contact the ambulance.',
  description='Contact the ambulance.',
  tools=[
     contact_ambulance_tool
  ]
)

MODEL = 'gemini-2.0-flash'

root_agent = Agent(
  name='iloilo_province_ambulance_support_agent',
  model=MODEL,
  instruction=prompt.AMBULANCE_SUPPORT_PROMPT,
  description='To provide ambulance support to the user by identifying and verifying the stated emergency, pinpointing their exact location and using it to search for a nearby hospital, and contacting the ambulance service.',
  tools=[
    AgentTool(agent=google_search_agent),
    AgentTool(agent=gps_location_agent),
    AgentTool(agent=contact_ambulance_agent)
  ],
)

