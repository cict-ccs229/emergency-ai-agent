# 🚑 Emergency Ambulance Assistant Agent

This project implements an emergency assistant agent using [Google's ADK (Agent Development Kit)](https://developers.generativeai.google). The agent is designed to help users request ambulance services quickly based on their current location.

---

## 📹 Video Demonstration

Link for my video on Google Drive: https://drive.google.com/drive/folders/1T8pE3JVNZi6UatP_cGTDSHR249qCdUCU?usp=sharing

---

## 📦 Features

- **📍 Location Detection (Mocked)**  
  Retrieves the user's approximate location using a mocked IP-based latitude and longitude.

- **🏥 Nearest Hospital Finder**  
  Uses the Haversine formula to calculate distances and identify the nearest hospital from a predefined list in Iloilo City.

- **🚨 Ambulance Dispatch Simulation**  
  Automatically contacts an ambulance at the closest hospital and notifies the user.

- **🗣️ Speech Output (Optional)**  
  Uses text-to-speech to vocalize the response (optional, for systems with voice capability).

---

## 🔧 Tools

| Tool Name                  | Description                                                              |
|----------------------------|--------------------------------------------------------------------------|
| `get_current_location_tool()` | Retrieves user's (mocked) geolocation data based on IP address.        |
| `search_nearby_hospitals()`   | Calculates the distance to hospitals and returns them sorted by proximity. |
| `contact_ambulance_tool()`    | Simulates contacting an ambulance at the closest hospital.             |
| `speech_synthesis()` (optional) | Speaks the agent's response using text-to-speech.                     |

---

## 🧠 How It Works (Agent Workflow)

1. **User Triggers the Request**  
   The user initiates an emergency request (e.g., "I need help, please call an ambulance").

2. **Agent Offers Assistance**  
   The agent asks:  
   > “Should I get your current location to find nearby hospitals?”

3. **Retrieve Location**  
   The `get_current_location_tool()` provides a mocked location (e.g., `{latitude: 10.7202, longitude: 122.5621}`).

4. **Find the Nearest Hospital**  
   The agent uses the Haversine formula to compute distances from the user to each hospital in the list:
   - Iloilo Mission Hospital
   - Western Visayas Medical Center
   - St. Paul Hospital - Iloilo

5. **Dispatch Ambulance**  
   The agent selects the closest hospital and calls `contact_ambulance_tool()` to simulate dispatching an ambulance:
   > “Ambulance dispatched to St. Paul Hospital - Iloilo based on your current location.”

6. **(Optional) Speak the Response**  
   If speech is enabled, the message is vocalized using `speech_synthesis()`.

---

## 🗺️ Predefined Hospitals

The agent currently includes a mock database of hospitals in Iloilo City:

```python
hospitals = {
    "Iloilo Mission Hospital": {"latitude": 10.7160, "longitude": 122.5642},
    "Western Visayas Medical Center": {"latitude": 10.7209, "longitude": 122.5596},
    "St. Paul Hospital - Iloilo": {"latitude": 10.7198, "longitude": 122.5615},
}
