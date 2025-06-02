import os
import random
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import BaseTool, google_search

# Load environment variables
load_dotenv()

# Shared emergency state (MUST BE AT TOP)
emergency_state = {
    "user_location": None,
    "emergency_verified": False,
    "emergency_type": None,
    "nearby_hospitals": [],
    "ambulance_contacted": False,
    "ambulance_eta": None
}

# === TOOL: First Aid Tips via Google Search ===
class FirstAidSearchTool(BaseTool):
    def call(self, injury: Optional[str] = "pilas") -> Dict[str, Any]:
        results = google_search(f"anong dapat himuon samtang nagahulat sang ambulansya para sa {injury}")
        return {"tips": results.get("results", [])}

first_aid_search_tool = FirstAidSearchTool(
    name="first_aid_search",
    description="Search what to do while waiting for the ambulance based on an injury keyword."
)

# === TOOL: Confirm Emergency ===
class ConfirmEmergencyTool(BaseTool):
    def call(self, description: str) -> Dict[str, Any]:
        emergency_state["emergency_verified"] = False
        return {
            "message": f"Pakiconfirm bala ni: '{description}'? Sabta lang 'yes' kung kinahanglan buligan, 'no' kung indi.",
            "memory_update": {"awaiting_confirmation": True}
        }

confirm_emergency_tool = ConfirmEmergencyTool(
    name="confirm_emergency",
    description="Ask the user to confirm the described emergency situation before proceeding."
)

# === TOOL: Contact Ambulance ===
class ContactAmbulanceTool(BaseTool):
    def call(self, hospital: str) -> Dict[str, Any]:
        approved = random.choice([True, False])
        eta_minutes = random.randint(5, 12)

        if approved:
            emergency_state["ambulance_contacted"] = True
            emergency_state["ambulance_eta"] = eta_minutes
            return {
                "message": f"Ambulansya halin sa {hospital} padulong na. Maabot mga {eta_minutes} minutos.",
                "follow_up": "Ano ang natabo? Ano nga pilas/aksidente?"
            }
        else:
            return {
                "message": f"Pasensya, indi makapa-dispatch sang ambulansya halin sa {hospital}. Pwede ta sulayan iban?"
            }

contact_ambulance_tool = ContactAmbulanceTool(
    name="contact_ambulance",
    description="Mock contact of ambulance from the given hospital. 50% chance of approval with ETA and injury follow-up."
)

# === TOOL: Get Current Location (Mock) ===
class GetCurrentLocationTool(BaseTool):
    def call(self, **kwargs) -> Dict[str, Any]:
        location = {"address": "Arevalo, Iloilo City"}
        emergency_state["user_location"] = location
        return {"location": {"address": location["address"]}}

get_current_location_tool = GetCurrentLocationTool(
    name="get_current_location",
    description="Retrieves the user's current location (address only; coordinates excluded)."
)

# === TOOL: Find Nearby Hospitals ===
class FindNearbyHospitalsTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        hospitals = {
            "molo": ["Medical City Iloilo", "Molo District Hospital"],
            "jaro": ["Iloilo Mission Hospital", "St. Clements Hospital"],
            "la paz": ["WVSU Medical Center", "Iloilo Doctor's Hospital"]
        }

        if not location_query:
            return {"error": "Wala sang lugar nga ginpasa para mangita hospital."}

        results = hospitals.get(location_query.strip().lower())
        if results:
            emergency_state["nearby_hospitals"] = results
            return {"hospitals": results}
        else:
            return {
                "hospitals": [],
                "note": "Wala sang kilala nga ospital sa sinang lugar. Ga pangita ko online...",
                "google_results": google_search(f"hospitals near {location_query}")
            }

find_nearby_hospitals_tool = FindNearbyHospitalsTool(
    name="find_nearby_hospitals",
    description="Returns a list of nearby hospitals based on a location keyword like 'Jaro', 'La Paz', or 'Molo'."
)

# === ROOT AGENT ===
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
Ikaw ang Iloilo Emergency AI Assistant. Voice kag text available. Ang mga user naga-istorya sa natural nga paagi.

**IMPORTANTE GUID:**
- Indi pag-isipon ang latitude/longitude. Lugar lang or address lang.
- Indi pagbaton sang request nga wala labot sa emergency (e.g., computer help, joke, etc.).

**FLOW:**
1. Sugod gamit `confirm_emergency(description: str)`
2. Hulat sang "yes" anay antes magpadayon.
3. Kung wala sang lugar, tawga `get_current_location()`.
4. Gamiton ang lugar sa `find_nearby_hospitals(location_query)`.
5. Tawga ang `contact_ambulance(hospital)`.
6. Mangayo info sa injury, tapos tawga `first_aid_search(injury)`.

**EXAMPLE:**
User: "May disgrasya sa Jaro!"
→ confirm_emergency("Disgrasya sa Jaro")
→ Hulat 'yes'
→ find_nearby_hospitals("Jaro")
→ contact_ambulance("Iloilo Mission Hospital")
→ "Padulong na ambulansya. ETA: 8 minutos. Ano natabo? May pilas?"

Magpabilin nga kalmado, klaro, kag madasig. Ang user pwede naga-panik.
"""
)
