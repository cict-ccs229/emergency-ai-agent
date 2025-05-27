import os
import random
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import BaseTool, google_search

load_dotenv()

emergency_state = {
    "user_location": None,
    "emergency_verified": False,
    "emergency_type": None,
    "nearby_hospitals": [],
    "ambulance_contacted": False,
    "ambulance_eta": None
}

# 1. Confirm emergency details with the user
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

# 2. Get current user location (mocked as fixed Roxas City location)
class GetCurrentLocationTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        location = {"address": "Barangay Baybay, Roxas City"}
        emergency_state["user_location"] = location
        return {"location": location}

get_current_location_tool = GetCurrentLocationTool(
    name="get_current_location",
    description="Retrieves the user's current location (address only; no coordinates)."
)

# 3. Find nearby hospitals based on user's location in Roxas City
class FindNearbyHospitalsTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        hospitals_by_area = {
            "arnaldo_blvd": ["Roxas Memorial Provincial Hospital"],
            "roxas_avenue": ["Capiz Emmanuel Hospital"],
            "lawaan": ["Medicus Medical Center Roxas", "Lawaan Birthing Center"],
            "tiza": ["Capiz Doctors' Hospital"],
            "banica": ["Banica Health Center"]
        }
        if not location_query:
            return {"error": "Location not provided for hospital search."}
        results = hospitals_by_area.get(location_query.strip().lower())
        if results:
            emergency_state["nearby_hospitals"] = results
            return {"hospitals": results}
        else:
            google_results = google_search(f"hospitals near {location_query} Roxas City Capiz")
            hospitals_online = google_results.get("results", [])
            return {
                "hospitals": [],
                "note": "No predefined hospitals found. Found these online:",
                "google_results": hospitals_online
            }

find_nearby_hospitals_tool = FindNearbyHospitalsTool(
    name="find_nearby_hospitals",
    description="Returns a list of nearby hospitals based on a location keyword like 'Baybay', 'Lawaan', 'Tiza', or 'Banica' in Roxas City."
)

# 4. Contact ambulance from a given hospital (mock dispatch with 50% chance)
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

# 5. Search first aid tips while waiting for ambulance based on injury keyword
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

# 6. Track ambulance status and ETA updates
class TrackAmbulanceTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        if not emergency_state["ambulance_contacted"]:
            return {"message": "No ambulance has been dispatched yet."}
        if emergency_state["ambulance_eta"] is None:
            return {"message": "ETA not available."}
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

# 7. Provide alternative transport options if ambulances are unavailable
class FindAlternativeTransportTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        alternatives = {
            "baybay": ["Baybay Tricycle Hotline: 0917-222-1111"],
            "lawaan": ["Lawaan Tricycle Operators: 0927-333-4444"],
            "tiza": ["Tiza Barangay Emergency: (036) 621-1234"],
            "banica": ["Banica Community Response: (036) 621-4321"]
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

# 8. Provide emergency hotlines specific to Roxas City
class GetEmergencyHotlinesTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        hotlines = {
            "PNP Roxas": "117 / (036) 621-2077",
            "BFP Roxas": "(036) 621-2311",
            "Roxas Memorial Provincial Hospital": "(036) 621-2078",
            "Red Cross Capiz Chapter": "(036) 621-2345",
            "City Ambulance Service": "(036) 621-4567"
        }
        return {"hotlines": hotlines}

get_emergency_hotlines_tool = GetEmergencyHotlinesTool(
    name="get_emergency_hotlines",
    description="Provides important emergency hotlines for Roxas City, Capiz."
)

# === Load AI instructions before creating the agent ===
instruction_path = os.path.join(os.path.dirname(__file__), "ambulance_ai-agent", "instructions.txt")
with open(instruction_path, "r") as f:
    emergency_agent_instruction = f.read()

# === Root Agent Definition for Roxas City ===
root_agent = Agent(
    name="roxas_emergency_ai",
    model="gemini-2.0-flash-exp",
    description="Main AI agent for handling ambulance dispatch in Roxas City, Capiz.",
    tools=[
        confirm_emergency_tool,          # 1
        get_current_location_tool,       # 2
        find_nearby_hospitals_tool,      # 3
        contact_ambulance_tool,          # 4
        first_aid_search_tool,           # 5
        track_ambulance_tool,            # 6
        find_alternative_transport_tool, # 7
        get_emergency_hotlines_tool,     # 8
        google_search                   # 9 external
    ],
    instruction=emergency_agent_instruction,
)
