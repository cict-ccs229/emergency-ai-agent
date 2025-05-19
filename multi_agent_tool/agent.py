from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search, agent_tool
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional
from .tts import toSpeech

def get_current_location_tool():
    pass


def contact_ambulance_tool():
    pass

def do_something_with_response(callback_context: CallbackContext, llm_response: LlmResponse):
    text = llm_response.content.parts[0].text
    
    if text:
        toSpeech(text)
    
    return None
    
search_agent = Agent(
    name='hospital_search_assistant',
    model='gemini-2.0-flash-exp',
    instruction='Your task is to search for the nearest hospital. The area is only within Iloilo City, Philippines.',
    tools=[google_search]
)

get_location_agent = Agent(
    name='get_location_assistant',
    model='gemini-2.0-flash-exp',
    instruction=
        """
            You are an official AI support agent for an emergency response team. 
            Your task is to verify and evaluate the emergency, and get the location of the user. 
            Keep the user calm and composed while you try to get his location, to be passed later to another agent
            for searching the nearest hospital.
        """,
    tools=[get_current_location_tool]
)

contact_ambulance_agent = Agent(
    name='contact_ambulance_assistant',
    model='gemini-2.0-flash-exp',
    instruction=
        """
            You are an official AI support agent for an emergency response team. 
            Your task is to contact the local ambulance service provided to you.
        """
    ,
    tools=[contact_ambulance_tool]
)

root_agent = Agent(
    name='emergency_ai_assistant',
    model='gemini-2.0-flash-exp',
    description='An AI emergency support agent for local ambulance services.',
    tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=get_location_agent), agent_tool.AgentTool(agent=contact_ambulance_agent),],
    after_model_callback=do_something_with_response
)

# I need to find the nearest hospital. Can you help me?
