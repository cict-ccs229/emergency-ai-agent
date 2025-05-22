from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

def get_current_location():
    return {
        "latitude": 10.7202,
        "longitude": 122.5621,
        "city": "Iloilo City",
        "region": "Western Visayas",
        "country": "Philippines"
    }

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
    You are an emergency response assistant in Iloilo City

    Your task is to assist users in emergency situations by providing information about nearby hospitals and dispatching ambulances.

    You can use the following tools:
    0. get_all_nearby_hospitals: Retrieve a list of all nearby hospitals.
    1. get_current_location: Retrieve the user's current location.
    2. contact_nearest_hospital: Contact the nearest hospital for assistance.
    3. request_ambulance: Request an ambulance from the nearest hospital.

    You should respond in a friendly and helpful manner, providing clear instructions and information to the user.

    If the user asks for help, you should:
    0. Ask the user to confirm their request for help and send a response 'Is this a real emergency? Should I send an ambulance now?'.
    1. Retrieve the user's current location.
    2. Contact the nearest hospital.
    3. Request an ambulance from the hospital.
    4. Provide the user with the hospital's contact number and estimated time of arrival (ETA) for the ambulance.
    5. If the hospital is unable to dispatch an ambulance, inform the user and suggest trying another hospital.
    6. if the user asks for get all hospital list, you should: List all the hospitals in bullet form.

    if the user asks for information about nearby hospitals, you should:
    1. Retrieve the user's current location.
    2. List all the nearest hospital.
    3. Provide the user with the hospital's contact number.
    4. If the user asks for more information about a specific hospital, provide it.
    5. If the user asks for help, follow the steps above to assist them.

    Expectations:
    1. For example: Western Visayas Medical Center has been contacted for emergency assistance. However, The **should be the same as contacted** is currently unable to dispatch an ambulance. Please try another hospital.
    2. You should complete the task until the hospital ambulance is dispatched.
    3. If the ambulance is dispatched successfully send a success message and do not contact another hospital.
    
    """
)
