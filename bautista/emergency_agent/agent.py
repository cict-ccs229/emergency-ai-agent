from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from datetime import datetime
import random
import asyncio
import requests
import pyttsx3  # Text-to-speech module

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"[TTS] {text}")
    engine.say(text)
    engine.runAndWait()

def get_ip_location():
    """Get approximate user location based on public IP address."""
    print("[DEBUG] get_ip_location called")
    try:
        response = requests.get("https://ipapi.co/json/")
        data = response.json()
        print(f"[DEBUG] IP location: {data}")
        return {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name")
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch IP location: {e}")
        return {
            "latitude": None,
            "longitude": None,
            "city": None
        }

async def get_current_location():
    """Async wrapper to get IP-based location."""
    return get_ip_location()

async def find_nearby_hospitals(params: dict):
    """Search for nearby hospitals based on coordinates (mock web search)."""
    latitude = params.get("latitude")
    longitude = params.get("longitude")
    print(f"[DEBUG] find_nearby_hospitals called with: lat={latitude}, long={longitude}")
    
    if latitude is None or longitude is None:
        return ["Location unavailable. Unable to list nearby hospitals."]
    
    try:
        # I utilized mock data for demonstration purposes. But we can also use google places API or similar services to fetch real data.
        # Uncomment the following lines to use a real API call
        # Simulated web API call to fetch nearby hospitals
        # Replace with actual API call if available, e.g. Google Places API
        # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&type=hospital&key=YOUR_API_KEY"
        # response = requests.get(url)
        # data = response.json()
        
        # MOCK data simulating API response
        data = {
            "results": [
                {"name": "QualiMed Hospital (Iloilo)"},
                {"name": "Iloilo Doctor’s Hospital"},
                {"name": "Medicus Medical Center"},
                {"name": "Iloilo Mission Hospital"},
                {"name": "St. Paul Hospital – Iloilo"},
                {"name": "The Medical City – Iloilo"},
                {"name": "Western Visayas Medical Center"},
                {"name": "Asia Pacific Medical Center – Iloilo"}
            ]
        }
        
        hospital_names = [place["name"] for place in data.get("results", [])]
        return hospital_names

    except Exception as e:
        print(f"[ERROR] Web search for hospitals failed: {e}")
        return ["Sorry, unable to fetch hospital information at this time."]

async def contact_ambulance(hospital: str):
    """Mock ambulance contact with 50% chance of approval."""
    print(f"[DEBUG] contact_ambulance called for: {hospital}")
    approved = random.choice([True, False])
    if approved:
        return {
            "status": "dispatched",
            "hospital": hospital,
            "eta": f"{random.randint(5, 15)} minutes",
            "contact": "09562637168",
        }
    else:
        return {
            "status": "unavailable",
            "reason": "All units currently responding",
        }

# Define tools for the agent
get_current_location_tool = FunctionTool(func=get_current_location)
find_nearby_hospitals_tool = FunctionTool(func=find_nearby_hospitals)
contact_ambulance_tool = FunctionTool(func=contact_ambulance)

# Create the emergency assistant agent
root_agent = Agent(
    name="emergency_agent",
    model="gemini-2.0-flash-exp",
    description="AI-powered emergency agent for Iloilo City, Philippines.",
    tools=[
        get_current_location_tool,
        find_nearby_hospitals_tool,
        contact_ambulance_tool,
    ],
    instruction=f"""
You are a voice-activated emergency assistant serving Iloilo City.

When a user requests ambulance or emergency help (e.g., “I need an ambulance,” “Send help,” “Emergency”):

1. Confirm the situation by asking:

    "Is this a real emergency? Should I dispatch an ambulance now?"

2. Based on the user’s response:
    - If yes:
        a. Attempt to determine their location using IP.
        b. Find nearby hospitals (only if location is known).
        c. Attempt to contact each hospital to send an ambulance.
        d. When an ambulance is dispatched, inform the user:

            "An ambulance from <hospital> is on the way and will arrive in approximately <eta>. Please stay on the line."

        e. If no ambulances are available, say:

            "Apologies, no ambulances are available right now. Please try again shortly."

        f. If the location cannot be determined, say:

            "Sorry, I couldn't determine your location. Please call emergency services directly."

    - If no:
        Reply politely:

            "Understood. No ambulance will be sent. Please stay safe."

3. If the user asks about nearby hospitals (e.g., “What hospitals are near me?”), respond with:

    "Here are some hospitals in Iloilo City:

    - QualiMed Hospital (Iloilo)
    - Iloilo Doctor’s Hospital
    - Medicus Medical Center
    - Iloilo Mission Hospital
    - St. Paul Hospital – Iloilo
    - The Medical City – Iloilo
    - Western Visayas Medical Center
    - Asia Pacific Medical Center – Iloilo"

Additional guidelines:
- Keep responses brief, clear, and conversational.
- You may mention the city for reassurance.
- Avoid disclosing raw coordinates or internal tool details.
- Do not answer unrelated or non-emergency queries.
- Maintain a calm and helpful tone.

Current date: {datetime.now().strftime("%B %d, %Y")}.
"""
)

# Handles retries for API rate limits
async def safe_chat(agent, user_input, retries=3, delay=25):
    for attempt in range(retries):
        try:
            response = await agent.chat(user_input)
            return response
        except Exception as e:
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg and attempt < retries - 1:
                print(f"[WARN] Rate limited by API. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                print(f"[ERROR] {error_msg}")
                return "Sorry, the service is currently overloaded. Please try again later."
    return "Sorry, the service is currently unavailable."

# Main test loop for interactive use
async def interactive_test():
    print("Emergency AI Agent test started. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() == "exit":
            print("Exiting test.")
            break

        response = await safe_chat(root_agent, user_input)
        print(f"Agent: {response}")
        speak(str(response))  # Speak the agent's response

if __name__ == "__main__":
    asyncio.run(interactive_test())
