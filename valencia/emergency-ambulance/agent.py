import os
from dotenv import load_dotenv
from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search
from .ambulance_tools import GetCurrentLocationTool, ContactAmbulanceTool

# ---- Load environment variables ----
load_dotenv()

def get_current_time() -> str:
    return datetime.now().strftime("%m-%d-%Y")

root_agent = Agent(
    name="ambulance_dispatch_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to handle emergency ambulance dispatch operations.",
    instruction=f"""
    You are an assistant that coordinates emergency ambulance dispatch in the Philippines.
    You get the nature of the accident and the user's location from the user.
    You will ask the user to confirm the accident before proceeding and the user can verify verbally, through text, or through an image.
    Immediately upon receiving the user's location, dispatch an ambulance.
    Give as well the information about the hospital dispatch origin and the estimated arrival time.
    For mock purposes, the ambulance dispatch will be approved 50% of the time.
    If denied, return only the reason for disapproval and ask the user if they want to contact another hospital.
    Strictly do not include the coordinates of the user in the output.
    Strictly adhere to the guideline of not catering to any other requests outside of the ambulance dispatch operations.

    ## Ambulance Dispatch Operations
    You can perform dispatch operations directly using these tools:
    - `get_current_location`: Retrieves the current GPS coordinates of the user.
    - `contact_ambulance`: Contacts the local ambulance service and dispatches an ambulance.
    - `google_search`: Searches for nearby hospitals based on location.

    ## Dispatch Guidelines
    - As soon as you receive the user's location, immediately contact the ambulance service.
    - If the ambulance dispatch is approved, provide details such as the hospital dispatch origin and the estimated arrival time.
    - If denied, return only the reason for disapproval and ask the user if they want to contact another hospital.
    - In the output, do not include the coordinates of the user.
    - If the user does not confirm the accident, do not proceed with the dispatch.
    - If the user does not want to contact another hospital, do not proceed with the dispatch.
    - Display the information in text in this format:
      "Ambulance dispatched from (hospital), ETA:  minutes."
    
    Be super concise in your responses.
    
    Today's date is {get_current_time()}.
    """,
    tools=[
        google_search,
        GetCurrentLocationTool(),
        ContactAmbulanceTool()
    ]
)

if __name__ == "__main__":
    # Confirm accident before proceeding.
    accident_confirmed = input("Accident confirmed at your location? (yes/no): ")
    if accident_confirmed.strip().lower() != "yes":
        print("Please confirm the accident before requesting an ambulance.")
        exit()
    
    # Get the user's location (but do not output the coordinates)
    location_tool = GetCurrentLocationTool()
    loc = location_tool.run()
    
    # Obtain nearby hospitals (assume google_search returns a list of hospital names)
    query = f"hospitals near {loc['latitude']}, {loc['longitude']}"
    hospitals = google_search(query)
    
    contact_tool = ContactAmbulanceTool()
    patient_info = {
        "location": loc,
        "condition": "unconscious, severe bleeding"
    }
    
    dispatched = False
    for hospital in hospitals:
        patient_info["hospital"] = hospital
        result = contact_tool.run(patient_info)
        if result.get("status") == "approved":
            print(f"Ambulance dispatched from {hospital}, ETA: {result.get('eta_minutes')} minutes.")
            dispatched = True
            break
        else:
            print(f"Ambulance dispatch denied by {hospital}.")
            next_choice = input("Contact another hospital? (yes/no): ")
            if next_choice.strip().lower() != "yes":
                break

    if not dispatched:
        print("I am unable to contact the ambulance directly. Please contact West Visayas State University Medical Center at (033) 320 2431 to request an ambulance.")
    
    # Use agent as a conversational partner:
    response = root_agent.chat("I need an ambulance")
    print(f"Agent response: {response}")