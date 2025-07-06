from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

# Get current location
def get_current_location():
    return {
        "latitude": 10.7202,
        "longitude": 122.5621,
        "city": "Iloilo City",
        "region": "Western Visayas",
        "country": "Philippines"
    }

# Get all nearby hospitals
def get_all_nearby_hospitals():
    hospitals = [
        {"name": "St. Paul's Hospital Iloilo", "contact": "+63 33 337 2741"},
        {"name": "The Medical City Iloilo", "contact": "+63 33 500 1000"},
        {"name": "Western Visayas Medical Center", "contact": "+63 33 321 2841"},
    ]
    return {
        "status": "success",
        "message": "Here are all the nearby hospitals:",
        "hospitals": hospitals
    }

# Contact nearest hospital
def contact_nearest_hospital():
    hospitals = [
        {"name": "St. Paul's Hospital Iloilo", "contact": "+63 33 337 2741"},
        {"name": "The Medical City Iloilo", "contact": "+63 33 500 1000"},
        {"name": "Western Visayas Medical Center", "contact": "+63 33 321 2841"},
    ]
    hospital = random.choice(hospitals)
    return {
        "status": "contacted",
        "hospital_name": hospital["name"],
        "hospital_contact": hospital["contact"],
        "message": f"Nearest hospital '{hospital['name']}' has been contacted for emergency assistance."
    }

# Request ambulance through hospital
def request_ambulance():
    hospital_response = contact_nearest_hospital()
    dispatch_success = random.choice([True, False])
    if dispatch_success:
        return {
            "status": "ambulance_dispatched",
            "hospital": hospital_response["hospital_name"],
            "contact_number": hospital_response["hospital_contact"],
            "eta": f"{random.randint(5, 15)} minutes",
            "message": f"Ambulance has been dispatched from {hospital_response['hospital_name']}."
        }
    else:
        return {
            "status": "dispatch_failed",
            "hospital": hospital_response["hospital_name"],
            "reason": f"{hospital_response['hospital_name']} is currently unable to dispatch an ambulance. Please try another hospital."
        }

# Register tools
get_all_nearby_hospitals_tool = FunctionTool(func=get_all_nearby_hospitals)
get_current_location_tool = FunctionTool(func=get_current_location)
contact_nearest_hospital_tool = FunctionTool(func=contact_nearest_hospital)
request_ambulance_tool = FunctionTool(func=request_ambulance)

# Define the agent
root_agent = Agent(
    name="iloilo_emergency_response_agent",
    model="gemini-2.0-flash-exp",
    description="Emergency response assistant in Iloilo City.",
    tools=[
        get_all_nearby_hospitals_tool,
        get_current_location_tool,
        contact_nearest_hospital_tool,
        request_ambulance_tool
    ],
    instruction="""
    You are an emergency response assistant in Iloilo City.

    Your task is to assist users in emergency situations by providing information about nearby hospitals and dispatching ambulances. You can also process voice commands.

    You should respond in a friendly and helpful manner, providing clear instructions and information to the user.

    You can use these tools:
    - get_current_location: Retrieves the user's current location.
    - get_all_nearby_hospitals: Lists all nearby hospitals with their contact numbers.
    - contact_nearest_hospital: Contacts the nearest hospital for assistance.
    - request_ambulance: Requests an ambulance from the contacted hospital.

    - Message formatting examples:
    - For example: Western Visayas Medical Center has been contacted for emergency assistance. However, Western Visayas Medical Center is currently unable to dispatch an ambulance. Please try another hospital.
    - For example: St. Paul's Hospital Iloilo has been contacted for emergency assistance. An ambulance has been dispatched from St. Paul's Hospital Iloilo. The contact number is +63 33 337 2741, and the estimated time of arrival for the ambulance is 12 minutes. Please stay safe and wait for the ambulance to arrive.
    - If the ambulance is dispatched successfully, send a success message and do not contact another hospital.
    - Ensure a polite, clear, and professional tone for all responses.

    Voice commands include:
    - 'Help, I need an ambulance!' or 'Send an ambulance!' will trigger the request for an ambulance.
    - 'List nearby hospitals' will list all nearby hospitals.
    - 'Contact [Hospital Name]' will allow the user to get information about a specific hospital.

    When processing requests:
    1. If the user asks for help, confirm if it’s a real emergency and if an ambulance should be dispatched.
    2. Retrieve the user's current location.
    3. Contact the nearest hospital for assistance.
    4. Request an ambulance from the hospital.
    5. Provide the user with the hospital's contact number and estimated time of arrival (ETA) for the ambulance.
    6. If the hospital is unable to dispatch an ambulance, inform the user and suggest trying another hospital.
    7. If the user asks for a list of hospitals, show all hospitals in bullet form with their contact numbers.
    8. If the user asks for more information about a specific hospital, provide it.

    For voice commands:
    - If the user says 'I need help', ask them: 'Is this a real emergency? Should I send an ambulance now?'
    - If the user says 'Find hospitals near me', retrieve and show the list of nearby hospitals.
    - If the user mentions a specific hospital, give them its contact details and any additional info available.
    - For example: Western Visayas Medical Center has been contacted for emergency assistance. However, The **should be the same as contacted** is currently unable to dispatch an ambulance. Please try another hospital.
    """
)
