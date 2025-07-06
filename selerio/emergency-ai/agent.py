import os
import random
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools import BaseTool, google_search

load_dotenv()

# Shared emergency state
emergency_state = {
    "user_location": None,
    "emergency_verified": False,
    "emergency_type": None,
    "nearby_hospitals": [],
    "ambulance_contacted": False,
    "ambulance_eta": None,
    "panic_detected": False,
    "contact_attempts": 0
}

# Tool 1: Emergency Confirmation & Panic Detection
class EmergencyVerificationTool(BaseTool):
    def call(self, description: str, user_input: str = "") -> Dict[str, Any]:
        panic_keywords = ["help", "please", "panic", "can't breathe", "scared", "help me", "dead"]
        panic_detected = any(keyword in user_input.lower() for keyword in panic_keywords)
        
        emergency_state["panic_detected"] = panic_detected
        emergency_state["emergency_verified"] = False
        
        if panic_detected:
            calming_message = (
                "Please stay calm. I'm here to help. "
                "Take a deep breath in... and out. "
                "You're safe now. What happened? Is anyone injured?"
            )
            return {
                "message": calming_message,
                "memory_update": {"awaiting_confirmation": True, "panic_mode": True},
                "speech": True
            }
        else:
            verification_message = f"Please confirm this emergency: '{description}'. Say 'yes' to continue, 'no' to cancel."
            return {
                "message": verification_message,
                "memory_update": {"awaiting_confirmation": True, "panic_mode": False},
                "speech": True
            }

confirm_emergency_tool = EmergencyVerificationTool(
    name="confirm_emergency",
    description="Confirms emergency and detects panic, providing calming support."
)

# Tool 2: Get Location (Philippines)
class GetCurrentLocationTool(BaseTool):
    def call(self, manual_location: Optional[str] = None) -> Dict[str, Any]:
        try:
            if manual_location:
                location = {"address": manual_location, "method": "manual"}
                emergency_state["user_location"] = location
                return {"location": location, "status": "success"}
            
            mock_locations = [
                "Jaro District, Iloilo City",
                "Mandurriao District, Iloilo City",
                "Molo District, Iloilo City", 
                "La Paz District, Iloilo City",
                "Arevalo District, Iloilo City",
                "City Proper, Iloilo City"
            ]
            detected_location = {"address": random.choice(mock_locations), "method": "gps"}
            emergency_state["user_location"] = detected_location
            
            return {"location": detected_location, "status": "success"}
            
        except Exception:
            return {
                "location": None,
                "status": "failed",
                "error": "Could not detect your location. Please tell me your city or district.",
                "fallback_needed": True
            }

get_current_location_tool = GetCurrentLocationTool(
    name="get_current_location",
    description="Gets user location using GPS or manual input."
)

# Tool 3: Find Nearby Hospitals
class FindNearbyHospitalsTool(BaseTool):
    def call(self, location_query: Optional[str] = None) -> Dict[str, Any]:
        philippine_hospitals = {
            "jaro": [
                {"name": "Iloilo Mission Hospital", "phone": "(033) 335-0471", "specialty": "General", "address": "Mission Hospital St, Jaro District"},
                {"name": "Western Visayas Medical Center", "phone": "(033) 321-0853", "specialty": "Government", "address": "Q. Abeto St, Jaro District"},
                {"name": "Metro Iloilo Hospital & Medical Center", "phone": "(033) 321-1527", "specialty": "General", "address": "Metropolis Ave, Jaro District"}
            ],
            "mandurriao": [
                {"name": "Iloilo Doctors' Hospital", "phone": "(033) 321-0676", "specialty": "General", "address": "Benigno Aquino Ave, Mandurriao District"},
                {"name": "Qualimed Hospital Iloilo", "phone": "(033) 509-6000", "specialty": "General", "address": "Benigno Aquino Ave, Mandurriao District"}
            ],
            "molo": [
                {"name": "The Medical City Iloilo", "phone": "(033) 329-1000", "specialty": "General", "address": "Molo Plaza Complex, Molo District"},
                {"name": "Molo District Hospital", "phone": "(033) 336-5424", "specialty": "Government", "address": "Molo District"}
            ],
            "la paz": [
                {"name": "West Visayas State University Medical Center", "phone": "(033) 320-0870", "specialty": "Teaching", "address": "Luna St, La Paz District"},
                {"name": "Angel Salazar Memorial General Hospital", "phone": "(033) 329-6045", "specialty": "Government", "address": "La Paz District"}
            ],
            "arevalo": [
                {"name": "Arevalo District Hospital", "phone": "(033) 336-2849", "specialty": "Government", "address": "Arevalo District"},
                {"name": "Iloilo Provincial Hospital", "phone": "(033) 321-8244", "specialty": "Government", "address": "Arevalo District"}
            ]
        }

        if not location_query:
            return {"error": "Location not provided for hospital search."}

        location_key = location_query.lower().replace("city", "").replace(",", "").strip()
        
        for key, hospitals in philippine_hospitals.items():
            if key in location_key or location_key in key:
                emergency_state["nearby_hospitals"] = hospitals
                return {
                    "hospitals": hospitals,
                    "location": location_query,
                    "count": len(hospitals)
                }

        try:
            search_results = google_search(f"hospitals near {location_query} Philippines emergency")
            return {
                "hospitals": [],
                "web_search_results": search_results,
                "note": f"No database match found for {location_query}. Using online search.",
                "fallback_used": True
            }
        except Exception:
            return {
                "error": f"Could not find hospitals for {location_query}",
                "suggestion": "Try calling emergency hotline 911 or Red Cross 143."
            }

find_nearby_hospitals_tool = FindNearbyHospitalsTool(
    name="find_nearby_hospitals",
    description="Finds hospitals in the Philippines using database and fallback search."
)

# Tool 4: Contact Ambulance
class ContactAmbulanceTool(BaseTool):
    def call(self, hospital: str, emergency_type: str = "general") -> Dict[str, Any]:
        emergency_state["contact_attempts"] += 1
        
        base_approval_rate = 0.5
        if emergency_type.lower() in ["cardiac", "stroke", "accident", "critical"]:
            base_approval_rate = 0.7
        
        approved = random.random() < base_approval_rate
        eta_minutes = random.randint(8, 25)
        
        if approved:
            emergency_state["ambulance_contacted"] = True
            emergency_state["ambulance_eta"] = eta_minutes
            
            return {
                "status": "success",
                "message": f"✅ Ambulance dispatched from {hospital}. Estimated arrival: {eta_minutes} minutes. Ref#: EMR-{random.randint(1000, 9999)}",
                "eta": eta_minutes,
                "reference_number": f"EMR-{random.randint(1000, 9999)}",
                "follow_up": "What type of emergency or injury is it?"
            }
        else:
            fallback_message = f"❌ Ambulance not available at {hospital}. "
            if emergency_state["contact_attempts"] < 3:
                fallback_message += "Trying the next hospital..."
            else:
                fallback_message += "Please call: Red Cross 143, MMDA 136, or your barangay hotline."
            
            return {
                "status": "failed",
                "message": fallback_message,
                "attempts": emergency_state["contact_attempts"],
                "alternative_numbers": ["Red Cross: 143", "MMDA: 136", "Emergency: 911"]
            }

contact_ambulance_tool = ContactAmbulanceTool(
    name="contact_ambulance",
    description="Attempts to contact ambulance, provides alternatives if unavailable."
)

# Emergency Agent Setup
root_agent = Agent(
    name="philippines_emergency_ai",
    model="gemini-2.0-flash-exp",
    description="Emergency AI for ambulance dispatch and assistance in the Philippines.",
    tools=[
        confirm_emergency_tool,
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool,
    ],
    instruction="""
You are an emergency response AI for the Philippines.

CONTEXT:
- No centralized EMS
- People panic and struggle to communicate
- Social media sometimes used for emergency help

RULES:
1. Handle medical emergencies in the Philippines
2. Speak calmly and clearly
3. Detect panic and respond accordingly
4. Guide step-by-step
5. Provide backup numbers when needed

FLOW:
1. Confirm emergency with speech
2. Calm user if panicking
3. Get user location
4. Find nearest hospital
5. Try contacting ambulance (50% success)
6. Retry or suggest alternative numbers
7. Offer first aid advice while waiting
"""
)
