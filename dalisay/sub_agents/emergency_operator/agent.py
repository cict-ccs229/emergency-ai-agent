import random

from google.adk.agents import Agent

from . import prompt

def contact_ambulance_tool(contact_number: str) -> dict:
  return {'status': 'success', 'report': 'Ambulance service contacted successfully'}, 200 if random.random() > 0.5 else {'status': 'error', 'report': 'Failed to contact ambulance service'}, 500

emergency_operator_agent = Agent(
  name='get_current_location_tool',
  model='gemini-2.0-flash',
  instruction=prompt.EMERGENCY_OPERATOR_PROMPT,
  description='Contact the ambulance.',
  tools=[
     contact_ambulance_tool
  ]
)