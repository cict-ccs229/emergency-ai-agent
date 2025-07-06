from google.adk.agents import Agent
from math import radians, cos, sin, asin, sqrt

# Mock data for hospitals in Iloilo City
hospitals = {
    "Iloilo Mission Hospital": {"latitude": 10.7160, "longitude": 122.5642},
    "Western Visayas Medical Center": {"latitude": 10.7209, "longitude": 122.5596},
    "St. Paul Hospital - Iloilo": {"latitude": 10.7198, "longitude": 122.5615},
}

# Returns the user's current location based on mocked IP address data
def get_current_location_tool() -> dict:
    print("Getting user location based on IP address (mock)...")
    return {"latitude": 10.7202, "longitude": 122.5621}

# Calculates the distance between two geographic coordinates using the Haversine formula
def haversine(loc1, loc2):
    lat1, lon1 = loc1["latitude"], loc1["longitude"]
    lat2, lon2 = loc2["latitude"], loc2["longitude"]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Earth radius in kilometers
    return c * r

# Sorts and returns the list of nearby hospitals based on proximity to the user's location
def search_nearby_hospitals(location: dict) -> list:
    sorted_hospitals = sorted(hospitals.keys(), key=lambda h: haversine(location, hospitals[h]))
    print(f"Nearest hospital found: {sorted_hospitals[0]}")
    return sorted_hospitals

# Simulates contacting an ambulance and returns a dispatch confirmation message
def contact_ambulance_tool(location: dict, hospital_name: str) -> str:
    return f"Ambulance dispatched to {hospital_name} based on your current location."

# Uses text-to-speech to read out a message and returns the spoken text
def speech_synthesis(text: str) -> str:
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return f"Spoken: {text}"

# Defines the root emergency response agent using Google's ADK
root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-exp",
    instruction=(
        "You are a helpful assistant for emergency ambulance requests. "
        "When a user needs help, ask if you should get their current location. "
        "If the user agrees, get the user's location by their IP address (mocked). "
        "Then find the nearest hospital from this list: "
        "'Iloilo Mission Hospital', 'Western Visayas Medical Center', 'St. Paul Hospital - Iloilo'. "
        "Contact ambulance at the nearest hospital and inform the user."
    ),
    description="An assistant that contacts ambulance services based on user's location.",
    tools=[get_current_location_tool, search_nearby_hospitals, contact_ambulance_tool],
)