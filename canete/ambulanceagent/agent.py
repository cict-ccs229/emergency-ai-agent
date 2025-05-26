import os
import random
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import BaseTool, google_search

# Load environment variables
load_dotenv()

# Shared emergency state
emergency_state = {
    "user_location": None,
    "emergency_verified": False,
    "emergency_type": None,
    "nearby_hospitals": [],
    "ambulance_contacted": False,
    "ambulance_eta": None
}

# === Tool 1: Confirm Emergency ===
class ConfirmEmergencyTool(BaseTool):
    def call(self, description: str) -> Dict[str, Any]:
        emergency_state["emergency_verified"] = False
        return {
            "message": f"Please confirm: '{description}'. Reply with 'yes' to proceed or 'no' to cancel.",
            "memory_update": {"awaiting_confirmation": True}
        }

confirm_emergency_tool = ConfirmEmergencyTool(
    name="confirm_emergency",
    description="Ask the user to confirm the described emergency situation before proceeding."
)

# === Tool 2: Get Current Location (Mocked, address only) ===
class GetCurrentLocationTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        location = {"address": "Arevalo, Iloilo City"}
        emergency_state["user_location"] = location
        return {"location": {"address": location["address"]}}

get_current_location_tool = GetCurrentLocationTool(
    name="get_current_location",
    description="Retrieves the user's current location (address only; coordinates excluded)."
)

# === Tool 3: Find Nearby Hospitals ===
class FindNearbyHospitalsTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        hospitals = {
            "molo": ["Medical City Iloilo", "Molo District Hospital"],
            "jaro": ["Iloilo Mission Hospital", "St. Clements Hospital"],
            "la paz": ["WVSU Medical Center", "Iloilo Doctor's Hospital"]
        }

        if not location_query:
            return {"error": "Location not provided for hospital search."}

        results = hospitals.get(location_query.strip().lower())
        if results:
            emergency_state["nearby_hospitals"] = results
            return {"hospitals": results}
        else:
            return {
                "hospitals": [],
                "note": "No predefined hospitals found. Searching online...",
                "google_results": google_search(f"hospitals near {location_query}")
            }

find_nearby_hospitals_tool = FindNearbyHospitalsTool(
    name="find_nearby_hospitals",
    description="Returns a list of nearby hospitals based on a location keyword like 'Jaro', 'La Paz', or 'Molo'."
)

# === Tool 4: Contact Ambulance ===
class ContactAmbulanceTool(BaseTool):
    def call(self, hospital: str) -> Dict[str, Any]:
        approved = random.choice([True, False])
        eta_minutes = random.randint(5, 12)

        if approved:
            emergency_state["ambulance_contacted"] = True
            emergency_state["ambulance_eta"] = eta_minutes
            return {
                "message": f"Ambulance from {hospital} dispatched. Estimated arrival: {eta_minutes} minutes.",
                "follow_up": "What injury has been sustained?"
            }
        else:
            return {"message": f"Unable to dispatch ambulance from {hospital}. Please try another hospital."}

contact_ambulance_tool = ContactAmbulanceTool(
    name="contact_ambulance",
    description="Mock contact of ambulance from the given hospital. 50% chance of approval with ETA and injury follow-up."
)

# === Tool 5: First Aid Tips via Google Search ===
class FirstAidSearchTool(BaseTool):
    def call(self, injury: Optional[str] = "injury") -> Dict[str, Any]:
        results = google_search(f"what to do while waiting for ambulance for {injury}")
        return {"tips": results.get("results", [])}

first_aid_search_tool = FirstAidSearchTool(
    name="first_aid_search",
    description="Search what to do while waiting for the ambulance based on an injury keyword."
)

# === Root Agent with Voice Support ===
root_agent = Agent(
    name="iloilo_emergency_ai",
    model="gemini-2.0-flash-exp",
    description="Main AI agent for handling ambulance dispatch in Iloilo.",
    tools=[
        confirm_emergency_tool,
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool,
        first_aid_search_tool,
        google_search
    ],
    instruction="""
You are the Iloilo Emergency AI Assistant. Voice input and output are enabled by default using ADK Web. Expect users to speak naturally or type.

Only respond to medical emergencies in Iloilo City.

**STRICT RULES:**
- Do NOT include or mention coordinates (like latitude/longitude). Refer only to area names or addresses.
- Do NOT answer unrelated requests (e.g., tech help, weather, news, jokes).

**FLOW:**
1. Start by calling `confirm_emergency(description: str)`.
2. Wait for user to say "yes" before continuing (use `memory.awaiting_confirmation = True`).
3. If location is unknown, call `get_current_location()` (address only).
4. Call `find_nearby_hospitals(location_query: str)` using the area.
5. Call `contact_ambulance(hospital: str)`, which replies with ETA and asks "What injury has been sustained?"
6. After user states the injury, call `first_aid_search(injury: str)`.

**EXAMPLE 1:**
User: "There's been a car crash in Molo."
→ confirm_emergency("Car crash in Molo")
→ (wait for yes)
→ find_nearby_hospitals("Molo")
→ contact_ambulance("Medical City Iloilo")
→ (responds with ETA + injury prompt)

**EXAMPLE 2:**
User: "Help! I need an ambulance!"
→ confirm_emergency("User requesting emergency assistance")
→ (wait for yes)
→ get_current_location()
→ find_nearby_hospitals(location_query)
→ contact_ambulance(hospital)
→ "Ambulance en route. ETA: 9 minutes. What injury has been sustained?"

Always stay calm, clear, and brief. The user may be under stress.
"""
)
