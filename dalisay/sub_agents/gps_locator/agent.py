import geocoder
from google.adk.agents import Agent

from . import prompt

def get_current_location_tool(location: str = 'me') -> dict:
  if location:
    g = geocoder.google(location)
  else:
    g = geocoder.ip(location)
  
  if g.ok:
      return { 'status': 'success', 'result': { 'latlong': g.latlng, 'city': g.city, 'country': g.country, 'address': g.address } }
  
  return { 'status': 'error', 'result': 'Geocoder failed to get the user\'s location. Fallback to what the user has given and use it for web searching hospitals'}

gps_locator_agent = Agent(
  name='gps_locator_agent',
  model='gemini-2.0-flash',
  instruction=prompt.GPS_LOCATOR_PROMPT,
  description='To pinpoint the exact location of the user using information they provided or through their IP Address.',
  tools=[
    get_current_location_tool
  ]
)