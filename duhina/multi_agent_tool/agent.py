from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search, FunctionTool, agent_tool
from google.adk.models import LlmResponse, LlmRequest
from typing import Optional
from .tts import toSpeech

from datetime import datetime


def get_current_location():
    return {"latitude": 10.7167, "longitude": 122.5639796}

def contact_ambulance():
    import random
    
    is_approved = random.choice([True, False])
    
    if is_approved:
        return {
            "status": "approved",
            "hospital": "Western Visayas Medical Center",
            "eta_minutes": random.randint(5, 20),
            "dispatch_id": f"DISPATCH-{random.randint(1000, 9999)}"
        }
    else:
        reasons = [
            "All ambulances currently deployed",
            "Location outside service area",
            "Technical difficulties in dispatch system",
            "No available medical staff"
        ]
        return {
            "status": "denied",
            "reason": random.choice(reasons)
        }

get_current_location_tool = FunctionTool(func=get_current_location)
contact_ambulance_tool = FunctionTool(func=contact_ambulance)

def do_something_with_response(callback_context: CallbackContext, llm_response: LlmResponse):
    text = llm_response.content.parts[0].text
    
    if text:
        toSpeech(text)
    
    return None

get_nearest_hospitals_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='GetNearestHospitalsAgent',
    description="Get the nearest hospital based on the user's location",
    tools=[google_search]
)

contact_and_location_agent = Agent(
    model='gemini-2.0-flash-exp',
    name='ContactNearestHospitalsAndGetLocationAgent',
    description="Contact the nearest hospital and get the user's location.",
    tools=[get_current_location_tool, contact_ambulance_tool]
)
    
root_agent = Agent(
    name='emergency_ai_assistant',
    model='gemini-2.0-flash-exp',
    description='An AI emergency support agent for local ambulance services.',
    instruction=f"""
            You are an assistant that coordinates local ambulance dispatch in Iloilo City, Philippines. 
            You need to get the nature of the accident (use `get_current_location_tool` to get the user's location. Don't ask for it).
            You have to verify the ambulance request if it is valid enough for an emergency. Use `google_search` for that.
            After receiving the user's location via `get_current_location()`, call an ambulance. 
            Give the location of the ambulance and ETA. 
            For the purpose of this demo, dispatch is random and will only be approved 50% of the time.
            
            Use the following tools:
            `google_search`: search for nearby hospitals based on location
            `get_current_location`: gets the GPS coords of the user
            `contact_ambulance`: Contacts local ambulance service
            
            Be super concise.
            Today's date is {datetime.now().strftime("%m-%d-%Y")}
        """,
    
    tools=[agent_tool.AgentTool(agent=get_nearest_hospitals_agent), get_current_location_tool, contact_ambulance_tool],
    after_model_callback=do_something_with_response
)

# I need to find the nearest hospital. Can you help me?
# I just got out of a car accident. I'm bleeding.