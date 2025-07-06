import os
import random
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

load_dotenv()

def get_location():
    print("[INFO] Retrieving user location (coordinates for Iloilo City)")
    return {"latitude": 10.7195, "longitude": 122.5522}

def find_hospitals(latitude: float, longitude: float):
    print(f"[INFO] Searching for hospitals near latitude {latitude}, longitude {longitude}")
    return [
        "West Visayas State University Medical Center",
        "Iloilo Mission Hospital",
        "Qualimed Iloilo"
    ]

def contact_ambulance(hospital: str):
    print(f"[INFO] Attempting to dispatch ambulance from hospital: {hospital}")
    approved = random.choice([True, False])
    if approved:
        return {
            "status": "approved",
            "hospital": hospital,
            "eta": f"{random.randint(10, 15)} minutes",
            "contact": "911",
        }
    else:
        return {
            "status": "denied",
            "reason": "All ambulances are currently unavailable. Do you want to contact another hospital?",
        }

# tools
location_tool = FunctionTool(get_location)
find_hospitals_tool = FunctionTool(find_hospitals)
contact_ambulance_tool = FunctionTool(contact_ambulance)


root_agent = Agent(
    name="ai_dispatch",
    model="gemini-2.0-flash-exp",
    description="AI assistant for ambulance dispatch in Iloilo Philippines",
    tools=[
        location_tool,
        find_hospitals_tool,
        contact_ambulance_tool,
    ],
    
    instruction=(
        f"You are an assistant that coordinates emergency ambulance dispatch in the Philippines.\n"
        f"You get the nature of the accident and the user's location from the user.\n"
        f"You will ask the user to confirm the accident before proceeding and the user can verify verbally or through text.\n"
        f"Only accept verified ambulance requests.\n"
        f"Immediately upon receiving the user's location, dispatch an ambulance.\n"
        f"Give as well the information about the hospital dispatch origin and the estimated arrival time.\n"
        f"For mock purposes, the ambulance dispatch will be approved 50% of the time.\n"
        f"If denied, return only the reason for disapproval and ask the user if they want to contact another hospital.\n"
        f"Strictly do not include the coordinates of the user in the output.\n"
        f"Strictly adhere to the guideline of not catering to any other requests outside of the ambulance dispatch operations.\n\n"
        f"## Ambulance Dispatch Operations\n"
        f"You can perform dispatch operations directly using these tools:\n"
        f"- `get_location`: Retrieves the current GPS coordinates of the user.\n"
        f"- `contact_ambulance`: Contacts the local ambulance service and dispatches an ambulance.\n"
        f"## Dispatch Guidelines\n"
        f"- As soon as you receive the user's location, immediately contact the ambulance service.\n"
        f"- If the ambulance dispatch is approved, provide details such as the hospital dispatch origin and the estimated arrival time.\n"
        f"- If denied, return only the reason for disapproval and ask the user if they want to contact another hospital.\n"
        f"- In the output, do not include the coordinates of the user.\n"
        f"- If the user does not confirm the accident, do not proceed with the dispatch.\n"
        f"- If the user does not want to contact another hospital, do not proceed with the dispatch.\n"
        f"- Display the information in text in this format:\n"
        f'  "Ambulance dispatched from (hospital), ETA:  minutes."\n\n'
        f"Be direct and very concise in your responses.\n\n"
        f"Never dispatch an ambulance unless the user has confirmed the accident."
    )
)
