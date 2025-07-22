import random

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

def contact_ambulance_tool(contact_number: str) -> dict:
    """Simulate contacting an ambulance service."""
    # Simulating a 50% chance of success or failure
    if random.random() > 0.5:
        return {'status': 'success', 'report': 'Ambulance service contacted successfully'}, 200
    else:
        return {'status': 'error', 'report': 'Failed to contact ambulance service'}, 500

call_agent = Agent(
    name='emergency_operator_agent',
    model='gemini-2.5-flash-preview-05-20',
    instruction='Contact the ambulance service.',
    description='Agent to contact the ambulance service in case of an emergency.',
    tools=[
        contact_ambulance_tool
    ],
)

call_agent_tool = AgentTool(agent=call_agent)