import os
import random
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import BaseTool, google_search

# === Load environment variables ===
load_dotenv()

# === Shared emergency state ===
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
        return {"location": location}

get_current_location_tool = GetCurrentLocationTool(
    name="get_current_location",
    description="Retrieves the user's current location (address only; no coordinates)."
)

# === Tool 3: Find Nearby Hospitals ===
class FindNearbyHospitalsTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        hospitals_by_area = {
            "molo": ["Medical City Iloilo", "Molo District Hospital"],
            "jaro": ["Iloilo Mission Hospital", "St. Clements Hospital"],
            "la paz": ["WVSU Medical Center", "Iloilo Doctor's Hospital"],
            "arevalo": ["Arevalo District Hospital"]
        }

        if not location_query:
            return {"error": "Location not provided for hospital search."}

        results = hospitals_by_area.get(location_query.strip().lower())
        if results:
            emergency_state["nearby_hospitals"] = results
            return {"hospitals": results}
        else:
            google_results = google_search(f"hospitals near {location_query}")
            hospitals_online = google_results.get("results", [])
            return {
                "hospitals": [],
                "note": "No predefined hospitals found. Found these online:",
                "google_results": hospitals_online
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
                "message": f"Ambulance from {hospital} dispatched. Estimated arrival: {eta_minutes} minutes."
            }
        else:
            return {
                "message": f"Unable to dispatch ambulance from {hospital}. Please try contacting a different hospital."
            }

contact_ambulance_tool = ContactAmbulanceTool(
    name="contact_ambulance",
    description="Mock contact of ambulance from the given hospital. 50% chance of approval with ETA and injury follow-up."
)

# === Tool 5: First Aid Tips via Google Search ===
class FirstAidSearchTool(BaseTool):
    def call(self, injury: Optional[str] = "injury") -> Dict[str, Any]:
        search_results = google_search(f"what to do while waiting for ambulance for {injury}")
        tips = search_results.get("results", [])
        return {
            "injury": injury,
            "tips": tips
        }

first_aid_search_tool = FirstAidSearchTool(
    name="first_aid_search",
    description="Searches what to do while waiting for the ambulance based on an injury keyword."
)

# === Tool 6: Track Ambulance Tool  ===

class TrackAmbulanceTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        if not emergency_state["ambulance_contacted"]:
            return {"message": "No ambulance has been dispatched yet."}

        if emergency_state["ambulance_eta"] is None:
            return {"message": "ETA not available."}

        # Simulate ETA countdown
        if emergency_state["ambulance_eta"] > 0:
            emergency_state["ambulance_eta"] -= random.randint(1, 3)
            if emergency_state["ambulance_eta"] < 0:
                emergency_state["ambulance_eta"] = 0

        if emergency_state["ambulance_eta"] == 0:
            return {"message": "Ambulance has arrived at your location."}
        else:
            return {"message": f"Ambulance ETA: {emergency_state['ambulance_eta']} minutes."}

track_ambulance_tool = TrackAmbulanceTool(
    name="track_ambulance",
    description="Tracks the ambulance's estimated arrival time and provides ETA updates."
)
# === Tool 7: Find Alternative Transport ===

class FindAlternativeTransportTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        alternatives = {
            "arevalo": ["Arevalo Tricycle Association Hotline: 0917-000-0001"],
            "molo": ["Molo Taxi Dispatch: (033) 335-6789"],
            "jaro": ["Jaro Emergency Center: (033) 320-3333"],
            "la paz": ["La Paz Barangay Health Center: (033) 337-1111"]
        }

        if not location_query:
            return {"error": "Location not provided for alternative transport search."}

        options = alternatives.get(location_query.strip().lower())
        if options:
            return {"alternatives": options}
        else:
            return {"message": "No alternative transport options found for the given area."}

find_alternative_transport_tool = FindAlternativeTransportTool(
    name="find_alternative_transport",
    description="Provides alternative transport or emergency options if no ambulance is available."
)

# === Tool 8: Get Emergency Hotlines ===

class GetEmergencyHotlinesTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        hotlines = {
            "PNP": "117 / (033) 337-1550",
            "BFP": "(033) 337-0999",
            "WVSU Medical Center": "(033) 320-0889",
            "Red Cross": "(033) 337-8175",
            "Iloilo Ambulance Service": "(033) 335-0451"
        }
        return {"hotlines": hotlines}

get_emergency_hotlines_tool = GetEmergencyHotlinesTool(
    name="get_emergency_hotlines",
    description="Provides important emergency hotlines for Iloilo City."
)

# === Load AI instructions ===
with open("ambulance_ai-agent/instructions.txt", "r") as f:
    emergency_agent_instruction = f.read()

# === Root Agent Definition ===
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
            track_ambulance_tool,
            find_alternative_transport_tool,
            get_emergency_hotlines_tool,
            google_search
        ],
        instruction=emergency_agent_instruction,
    )