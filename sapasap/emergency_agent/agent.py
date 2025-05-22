from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from datetime import datetime
import os
import random
from dotenv import load_dotenv

load_dotenv()

async def get_current_location():
    """Retrieve the user's approximate location (Iloilo City)."""
    print("[DEBUG] get_current_location called")
    return {"latitude": 10.7195, "longitude": 122.5522}   # Iloilo City coordinates


async def find_nearby_hospitals(latitude: float, longitude: float):
    """List hospitals near the provided coordinates."""
    print(f"[DEBUG] find_nearby_hospitals called with: lat={latitude}, long={longitude}")
    return [
        "West Visayas State University Medical Center",
        "Iloilo Mission Hospital",
        "Western Visayas Medical Center",
    ]


async def contact_ambulance(hospital: str):
    """Contact the Hospital and dispatch an ambulance."""
    print(f"[DEBUG] contact_ambulance called for: {hospital}")
    approved = random.choice([True, False])
    if approved:
        return {
            "status": "dispatched",
            "hospital": hospital,
            "eta": f"{random.randint(20, 30)} minutes",
            "contact": " 098 765 4321",
        }
    else:
        return {
            "status": "unavailable",
            "reason": "All units currently responding",
        }
#Tools for the agent
get_current_location_tool = FunctionTool(func=get_current_location)
find_nearby_hospitals_tool = FunctionTool(func=find_nearby_hospitals)
contact_ambulance_tool = FunctionTool(func=contact_ambulance)


#Initialize the agent
root_agent = Agent(
    name="emergency_agent",
    model="gemini-2.0-flash-exp",
    description="AI-powered emergency agent for Iloilo City, Philippines.",
    tools=[
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool,
    ],
    instruction=f"""
You are a voice-friendly emergency response assistant for Iloilo City.

When a user asks for an ambulance or emergency help (e.g. “I need an ambulance”, “Send help”, “Emergency”), follow these steps:

1. First, ask the user clearly:

    "Is this a real emergency? Should I send an ambulance now?"

2. Wait for the user’s response:
    - If the user says **yes**, proceed:
        a. Call `get_current_location` to determine their location (never reveal coordinates).
        b. Use `find_nearby_hospitals(latitude, longitude)` to list nearby hospitals.
        c. For each hospital, attempt `contact_ambulance(hospital)` in order.
        d. As soon as one responds with `"status": "dispatched"`, reply:

            "<hospital> – arriving in <eta>. Stay on the line for further instructions."

        e. If **no ambulances are available**, respond:

            "Sorry, no ambulances are available right now. Please try again later."

    - If the user says **no**, respond politely:

        "Okay, no ambulance will be sent. Stay safe."

3. If the user asks about hospitals (e.g. “What hospitals are near me?”), say:

    "Here are some hospitals in Iloilo City:
    - West Visayas State University Medical Center
    - Iloilo Mission Hospital
    - Western Visayas Medical Center"

Guidelines:
- Keep all responses short and natural, especially for voice output.
- Never mention function names, tools, or coordinates.
- Do not respond to non-emergency or off-topic queries.
- Speak clearly and support natural voice patterns.

Current date: {datetime.now().strftime("%B %d, %Y")}.
"""
)
