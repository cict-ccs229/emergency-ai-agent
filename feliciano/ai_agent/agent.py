import os
import random
import sys
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search

import aiohttp

if sys.platform.startswith("win"):
    # Use ProactorEventLoop (default in 3.8+ but let's force it)
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

# -- OpenStreetMap Nominatim geocoding --
async def geocode_location(location_name: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_name,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }
    headers = {
        "User-Agent": "EmergencyAgent/1.0 (ashleydenise.feliciano@gmail.com)"  # <-- Replace with your info
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            if resp.status == 200:
                results = await resp.json()
                if results:
                    lat = float(results[0]["lat"])
                    lon = float(results[0]["lon"])
                    return {"latitude": lat, "longitude": lon}
                else:
                    print("Assistant: Sorry, I couldn't find that location.")
                    return None
            else:
                print(f"Assistant: Error {resp.status} from location service.")
                return None

# -- Mock ambulance contact --
async def contact_ambulance(hospital: str):
    print(f"[DEBUG] contact_ambulance called for: {hospital}")
    approved = random.choice([True, False])
    if approved:
        return {
            "status": "dispatched",
            "hospital": hospital,
            "eta": f"{random.randint(10, 20)} minutes"
        }
    else:
        return {
            "status": "denied",
            "reason": "All units currently busy"
        }

# -- Wrap tools --
geocode_tool = FunctionTool(func=geocode_location)
contact_tool = FunctionTool(func=contact_ambulance)

# -- Agent Setup --
root_agent = Agent(
    name="emergency_dispatcher",
    model="gemini-2.0-flash-exp",
    description="Suggests nearest hospitals and offers ambulance dispatch",
    tools=[geocode_tool, contact_tool, google_search],
    instruction=f"""
You are a friendly emergency assistant.

If the user asks for help:
1. Ask: "Where are you currently located?"
2. Use `geocode_location(location_name)` to get coordinates.
3. Use `google_search("hospitals near <lat>, <long>")` to get nearby hospitals.
4. Suggest the first hospital from the list.
5. Ask: "Do you want me to try calling an ambulance from there?"
6. If yes, try `contact_ambulance(hospital)`:
    - If approved: show ETA and hospital name.
    - If denied: show reason and offer to try another hospital.
7. If the user says no: politely end.

Always be polite, short, and reassuring.
Do not reveal coordinates.
Today’s date is {datetime.now().strftime('%B %d, %Y')}.
"""
)

# -- Async Main Function --
async def main():
    print("User: I need help, there's an emergency!")

    user_location = input("Assistant: Where are you currently located? (e.g., Molo, Iloilo City): ").strip()
    location = await geocode_location(user_location)

    if not location:
        print("Assistant: Sorry, could not determine your location.")
        return

    query = f"hospitals near {location['latitude']}, {location['longitude']}"
    hospitals = google_search(query)

    if not hospitals:
        print("Assistant: Sorry, I couldn't find nearby hospitals.")
        return

    first_hospital = hospitals[0]
    print(f"Assistant: The nearest hospital is {first_hospital}.")

    dispatch = input(f"Assistant: Do you want me to try calling an ambulance from {first_hospital}? (yes/no): ").strip().lower()

    if dispatch == "yes":
        result = await contact_ambulance(first_hospital)
        if result["status"] == "dispatched":
            print(f"Assistant: Ambulance dispatched from {result['hospital']}, ETA: {result['eta']}. Stay calm.")
        else:
            print(f"Assistant: Ambulance not available – {result['reason']}.")
            try_next = input("Assistant: Should I try another hospital? (yes/no): ").strip().lower()
            if try_next == "yes":
                for hospital in hospitals[1:]:
                    retry = await contact_ambulance(hospital)
                    if retry["status"] == "dispatched":
                        print(f"Assistant: Ambulance dispatched from {retry['hospital']}, ETA: {retry['eta']}.")
                        break
                else:
                    print("Assistant: Sorry, no ambulances available right now. Please call emergency services directly.")
            else:
                print("Assistant: Okay, stay safe and call emergency services if needed.")
    else:
        print("Assistant: Okay, I won't call an ambulance. Let me know if you need anything else.")

# -- Run async entry point --
if __name__ == "__main__":
    asyncio.run(main())
