import random
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search, BaseTool

class GetCurrentLocationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="get_current_location_tool", 
            description="Simulates retrieving the user\'s current location in Iloilo City. Returns a dictionary with the location string."
        )
    
    def run(self) -> dict:
        mock_location_str = "Boardwalk, Mandurriao, Iloilo City, Iloilo, Philippines"
        print(f"[Tool Output] Current location determined as: {mock_location_str}")
        return {"location_string": mock_location_str}

class FindNearbyHospitalsTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="find_nearby_hospitals_tool",
            description="Finds nearby hospitals based on a location string. Returns a list of hospital objects, each with 'name' and 'phone'."
        )

    def run(self, input_data: dict) -> dict:
        location_string = input_data.get("location_string", "")
        print(f"[Tool Action] Finding hospitals near: {location_string} (mocked)")
        hospitals_data = [
            {"name": "West Visayas State University Medical Center", "phone": "09171234501"},
            {"name": "Iloilo Mission Hospital", "phone": "09181234502"},
            {"name": "Iloilo Doctors Hospital", "phone": "09191234503"}
        ]
        print(f"[Tool Output] Found hospitals: {hospitals_data}")
        return {"hospitals": hospitals_data}

class ContactAmbulanceTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="contact_ambulance_tool", 
            description="Simulates contacting an ambulance service. Expects input_data with keys: 'hospital_name', 'user_location', 'emergency_details'. Mock tool with 50% success."
        )
    
    def run(self, input_data: dict) -> dict:
        hospital_name = input_data.get("hospital_name", "Unknown Hospital")
        user_location = input_data.get("user_location", "Unknown Location")
        emergency_details = input_data.get("emergency_details", "No details provided")

        print(f"[Tool Action] Attempting to contact ambulance for {hospital_name}...")
        print(f"[Tool Action] User location: {user_location}")
        print(f"[Tool Action] Emergency details: {emergency_details}")

        if random.random() < 0.5:
            success_message = f"Successfully contacted {hospital_name}. An ambulance is (simulated to be) on its way to {user_location} for: {emergency_details}."
            print(f"[Tool Output] {success_message}")
            return {"status": "success", "message": success_message}
        else:
            failure_message = f"Failed to contact ambulance service for {hospital_name}. Please try another hospital or contact emergency services directly."
            print(f"[Tool Output] {failure_message}")
            return {"status": "failure", "message": failure_message}

load_dotenv()

# --- Agent Definition ---

root_agent = Agent(
    name="philippine_emergency_ambulance_support_agent",
    model="gemini-2.0-flash", 
    instruction="""You are an AI assistant dedicated to helping users in the Philippines contact ambulance services during medical emergencies in Iloilo City.
    Your primary goal is to reduce the time and complexity of getting help.

    Follow these steps:
    1.  First, calmly ask the user to describe their emergency. Assess if it's a medical emergency requiring an ambulance.
    2.  If it is, express empathy and reassure them you will help.
    3.  Then, use the 'get_current_location_tool'. This tool will return a dictionary containing a 'location_string'.
    4.  Once you have the location string, use 'find_nearby_hospitals_tool' with the 'location_string' to get a list of hospitals. This tool will return a dictionary with an 'hospitals' key containing a list of hospital objects. Each object will have a 'name' and a 'phone' number.
    5.  Present the hospital options to the user, including their names and phone numbers.
    6.  Ask the user to choose a hospital to contact for an ambulance, or if they prefer to call one of the hospitals directly using the provided number.
    7.  If they choose a hospital for you to contact, use the 'contact_ambulance_tool' to (simulate) contacting the ambulance service for that hospital. You need to provide the hospital's 'name', the 'user_location' (which is the location_string you obtained earlier), and the 'emergency_details' they shared.
    8.  The 'contact_ambulance_tool' will return a dictionary. Check the 'status' key. Inform the user of the outcome based on the 'message' key.
    9.  If the contact status is 'failure', suggest trying another hospital or dialing the national emergency hotline (e.g., 911 in the Philippines) directly.
    10. Maintain a calm, clear, and supportive tone throughout the interaction. Prioritize getting the necessary information efficiently but without causing more distress.
    """,
    description="An AI agent to assist with ambulance support in Iloilo City, Philippines. It can find nearby hospitals (mocked, with phone numbers) and simulate contacting ambulance services.",
    tools=[
        google_search, 
        GetCurrentLocationTool(), 
        FindNearbyHospitalsTool(),
        ContactAmbulanceTool()  
    ],
)

if __name__ == "__main__":
    print("--- Simulating Agent Flow (Manual Tool Calls) ---")

    retrieved_api_key = os.environ.get("GOOGLE_API_KEY")
    if retrieved_api_key:
        print(f"[INFO] GOOGLE_API_KEY found: {retrieved_api_key[:4]}...{retrieved_api_key[-4:]} (This is just for demonstration)")
    else:
        print("[INFO] GOOGLE_API_KEY not found. Ensure .env file is set up correctly and contains GOOGLE_API_KEY.")

    simulated_emergency_details = "Someone in Mandurriao, Iloilo City, has collapsed and is unresponsive."
    print(f"User: {simulated_emergency_details}")

    print("\nAgent: I understand. I'll help you. First, let me get your current location.")
    location_tool_instance = GetCurrentLocationTool()
    location_data = location_tool_instance.run()
    current_location = location_data["location_string"]
    print(f"Agent sees location data: {location_data}")

    print("\nAgent: Great! I've got your location. Now, let me find nearby hospitals.")
    hospitals_tool_instance = FindNearbyHospitalsTool()
    hospitals_data_result = hospitals_tool_instance.run({"location_string": current_location})
    hospitals_list = hospitals_data_result["hospitals"]
    print(f"Agent found hospitals data: {hospitals_list}")

    print("\nAgent: Here are some hospitals near you:")
    for i, hospital_info in enumerate(hospitals_list):
        print(f"{i+1}. {hospital_info['name']} - Phone: {hospital_info['phone']}")

    # Enhanced simulation for choosing hospital
    chosen_hospital_object = None
    while not chosen_hospital_object:
        try:
            hospital_choice_input = input("\nAgent: Which hospital would you like me to contact for an ambulance? Please enter the number: ")
            choice_index = int(hospital_choice_input) - 1
            if 0 <= choice_index < len(hospitals_list):
                chosen_hospital_object = hospitals_list[choice_index]
            else:
                print("Agent: Invalid number. Please choose from the list.")
        except ValueError:
            print("Agent: Invalid input. Please enter a number.")

    chosen_hospital_name = chosen_hospital_object["name"]
    print(f"User chose to contact: {chosen_hospital_name}")

    print(f"\nAgent: Great! I'll contact the ambulance service for {chosen_hospital_name}.")
    contact_tool_instance = ContactAmbulanceTool()
    contact_data = contact_tool_instance.run({"hospital_name": chosen_hospital_name, "user_location": current_location, "emergency_details": simulated_emergency_details})

    if contact_data["status"] == "success":
        print("\nAgent: The ambulance service has been contacted successfully!")
        print(f"Message: {contact_data['message']}")
    else:
        print("\nAgent: I'm sorry, but I couldn't contact the ambulance service.")
        print(f"Message: {contact_data['message']}")

    print("\nAgent: Thank you for using our service. I hope you get the help you need.") 