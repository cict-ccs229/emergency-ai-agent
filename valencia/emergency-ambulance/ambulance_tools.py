from google.adk.tools import BaseTool
import random

class GetCurrentLocationTool(BaseTool):
    def __init__(self):
        super().__init__(name="get_current_location", description="Retrieves the current GPS coordinates of the user.")
    
    def run(self, input: dict = None) -> dict:
        # Replace with actual location logic in production.
        return {"latitude": 14.5995, "longitude": 120.9842}

class ContactAmbulanceTool(BaseTool):
    def __init__(self):
        super().__init__(name="contact_ambulance", description=(
            "Contacts the local ambulance service and dispatches an ambulance with a 50% approval rate. "
            "If approved, returns dispatch details including the hospital dispatch origin and ETA; "
            "if denied, returns a reason for disapproval."
        ))
    
    def run(self, patient_info: dict) -> dict:
        approved = random.choice([True, False])
        if approved:
            hospital = "General Hospital"
            eta_minutes = random.randint(5, 15)
            return {
                "status": "approved",
                "hospital": hospital,
                "eta_minutes": eta_minutes
            }
        else:
            reasons = [
                "All ambulances are currently engaged in emergencies.",
                "Insufficient ambulance availability due to high demand.",
                "Our ambulances are all on duty at the moment."
            ]
            reason = random.choice(reasons)
            return {
                "status": "denied",
                "message": f"Ambulance dispatch denied: {reason} Please try again or call directly."
            }