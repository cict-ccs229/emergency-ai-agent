import random
from google.adk.agents import Agent
from google.adk.tools import FunctionTool # Import FunctionTool

# Tool to simulate getting the user's current location
def get_current_location_function(): 
    """Returns the user's current latitude and longitude."""
    return {
        "latitude": 10.7202,
        "longitude": 122.5621
    }

def find_hospital(latitude: float, longitude: float): 
    """Finds nearby hospitals based on the provided coordinates."""
    return ["West Visayas State Medical Center", "Iloilo Doctors' Hospital", "St. Paul's Hospital Iloilo", "The Medical City Iloilo", "Qualimed Hospital Iloilo"]

# Tool to simulate contacting an ambulance with 50% success rate
def contact_ambulance_function(hospital_name: str): 
    """Attempts to contact the ambulance service for the given hospital. Returns success or failure randomly."""
    success = random.choice([True, False])
    if success:
        return f"Ambulance from {hospital_name} has been dispatched to your location."
    else:
        return f"Unable to contact ambulance from {hospital_name}. Trying another hospital."

# Convert the function into a FunctionTool
contact_ambulance_tool = FunctionTool(
    func=contact_ambulance_function
)
get_current_location_tool = FunctionTool(
    func=get_current_location_function
)
find_hospital_tool = FunctionTool(
    func=find_hospital
)

# Root agent definition
root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-exp",
    description="An assistant to contact local ambulance services",
    tools=[find_hospital_tool, get_current_location_tool, contact_ambulance_tool], # Pass the FunctionTool objects
    instruction=f"""
    You are a helpful assistant that helps users in medical emergencies.
    Do not respond with any unncessary information.
    Do not introduce yourself.
    Your sole purpose is to help users in medical emergencies by contacting local ambulance services.
    You will coordinate users and ambulance dispatch services in the Philippines.
    Identify if user input is a medical emergency.
    If it is not, respond with "I can only assist in medical emergencies."
    You are to confirm if an ambulance is needed.
    Do not ask user for their location, use get_current_location_tool immediately their location.
    After getting user's location, use find_hospital_tool to locate the nearest ambulance to user's location.
    You will use contact_ambulance_tool to contact the ambulance service.
    If the ambulance service is not reachable, Notify user what hospital is unavailable and you will use contact_ambulance_tool again until another hospital is able to respond.
    Do not entertain any other request other than contacting ambulance services.
    Respond as concise as possible.
    """
)