# 🚨 Philippines Emergency Dispatch AI

This project is an AI-powered emergency response system built using the **Google AI Development Kit (ADK)**. It simulates real-time assistance for users in the Philippines — helping them confirm emergencies, detect panic, find nearby hospitals, and attempt ambulance dispatch.

> 🎥 Video Explanation:  https://youtu.be/PeFseokSVKQ
> 🏥 Target area: **Iloilo City, Philippines**  
> ⚙️ Built with: `Python`, `Google ADK`, `dotenv`, `custom tools`

---

## 📌 Features

- 🧠 **Panic Detection & Emotional Support**  
  Detects panic-related phrases and responds with calming messages.

- 📍 **Smart Location Retrieval**  
  Gets the user’s district (via mock GPS or manual input).

- 🏥 **Hospital Lookup**  
  Matches nearby hospitals from a predefined Iloilo hospital database or performs a Google search if no match is found.

- 🚑 **Ambulance Dispatch Simulation**  
  Attempts to contact ambulances based on urgency and hospital availability. Fallback numbers (e.g. 143, 911) are provided when needed.

---

## 🛠️ Tools Defined

### 1. `EmergencyVerificationTool`
- Detects panic using keywords like `help`, `can't breathe`, etc.
- Confirms emergency if no panic is detected.

### 2. `GetCurrentLocationTool`
- Retrieves location via:
  - Manual input
  - Mock GPS (e.g. “Jaro District, Iloilo City”)

### 3. `FindNearbyHospitalsTool`
- Searches Iloilo hospitals by district.
- Falls back to Google Search for unmatched locations.

### 4. `ContactAmbulanceTool`
- Simulates ambulance availability.
- Prioritizes critical emergencies (e.g. cardiac, accident).
- Retries or suggests emergency hotlines after 3 failed attempts.

---

## 🧠 Agent Configuration

```python
Agent(
  name="philippines_emergency_ai",
  model="gemini-2.0-flash-exp",
  description="Emergency AI for ambulance dispatch and assistance in the Philippines.",
  tools=[confirm_emergency_tool, get_current_location_tool, find_nearby_hospitals_tool, contact_ambulance_tool],
  instruction="""
    You are an emergency response AI for the Philippines.

    CONTEXT:
    - No centralized EMS
    - People panic and struggle to communicate
    - Social media sometimes used for emergency help

    RULES:
    1. Handle medical emergencies in the Philippines
    2. Speak calmly and clearly
    3. Detect panic and respond accordingly
    4. Guide step-by-step
    5. Provide backup numbers when needed

    FLOW:
    1. Confirm emergency with speech
    2. Calm user if panicking
    3. Get user location
    4. Find nearest hospital
    5. Try contacting ambulance (50% success)
    6. Retry or suggest alternative numbers
    7. Offer first aid advice while waiting
"""
)
