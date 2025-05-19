from google.adk.agents import Agent
from google.adk.tools import google_search, FunctionTool
from datetime import datetime
import random
from google.adk.tools.agent_tool import AgentTool  


# ---- TOOL DEFINITIONS ----

def get_current_location():
    """Returns the user's current location in Iloilo."""
    return {
        "latitude": 10.7202,
        "longitude": 122.5621
    }

def find_nearby_hospitals(latitude: float, longitude: float):
    """Returns a list of nearby hospitals near the given coordinates."""
    return [
        "West Visayas State University Medical Center",
        "Iloilo Mission Hospital",
        "St. Paul's Hospital Iloilo"
    ]

def contact_ambulance(hospital: str):
    """Attempts to dispatch an ambulance from the specified hospital."""
    is_approved = random.choice([True, False])
    if is_approved:
        return {
            "status": "dispatched",
            "hospital": hospital,
            "eta": f"{random.randint(5, 15)} minutes",
            "contact": "(033) 320 2431"
        }
    else:
        return {
            "status": "unavailable",
            "reason": "All units currently responding"
        }

# ---- TOOL WRAPPERS ----

get_current_location_tool = FunctionTool(func=get_current_location)
find_nearby_hospitals_tool = FunctionTool(func=find_nearby_hospitals)
contact_ambulance_tool = FunctionTool(func=contact_ambulance)

# ---- AGENTS ----

get_nearest_hospitals_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="GetNearestHospitalsAgent",
    description="Gets nearby hospitals using location given by user",
    tools=[google_search]
)

dispatch_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="IloiloAmbulanceDispatchAgent",
    description="Dispatches ambulance and handles emergencies.",
    tools=[
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool
    ],
    instruction=f"""
You are an AI assistant for emergency ambulance dispatch in Iloilo City.

- Analyze the user input, if it does not contain a location ask for it.
- Use `get_current_location` immediately to retrieve the user’s location.
- Use `find_nearby_hospitals(latitude, longitude)` to find possible hospitals near the user's provided location.
- Attempt `contact_ambulance(hospital)` for each one and choose the fastest and nearest hospital.
- If approved, respond like:
  "Ambulance dispatched from [hospital]. ETA: [eta]. Contact: [contact]."
- If all hospitals are unavailable, say:
  "Palihug tawag sa WVSU Medical Center sa (033) 320 2431."

NEVER show or say the user’s coordinates.

Only help with emergencies. Be brief and direct.

Date: {datetime.now().strftime("%B %d, %Y")}
"""
)

# ---- ROOT AGENT ----

root_agent = Agent(
    name="iloilo_emergency_ai",
    model="gemini-2.0-flash-exp",
    description="Main AI for handling emergency ambulance operations.",
    tools=[
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool,
        AgentTool(agent=get_nearest_hospitals_agent)  
    ],
    instruction=f"""
You are the Iloilo Emergency AI Assistant.

Ask the user: "Kumusta ang emergency? (What is the emergency?)"

Do not ask for location. Use `get_current_location` right away.

Proceed to dispatch an ambulance via `contact_ambulance(hospital)` after getting hospitals from `find_nearby_hospitals`.

Only respond with text like:
  "Ambulance dispatched from [hospital]. ETA: [eta]. Contact: [contact]."

If none succeed, respond:
  "Palihug tawag sa WVSU Medical Center sa (033) 320 2431."

Avoid using coordinates or extra information. Keep it clear and local.
"""
)

# ---- SAMPLE RUN ----

if __name__ == "__main__":
    print("Agent initialized.")
    response = root_agent.chat("Nabungguan ako, kinanlan ko ambulansya")
    print("Agent response:", response)
