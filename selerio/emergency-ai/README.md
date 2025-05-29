# 🇵🇭 Philippines Emergency AI Agent

This project is an **Emergency Response AI Agent** tailored for use in the **Philippines**. It is designed to detect emergencies, locate the user, find nearby hospitals, and simulate contacting an ambulance—all while handling panic situations and offering calm guidance.

> ⚠️ **Note**: This is a prototype/demo system and does not connect to real emergency services. It's meant for simulation, research, or educational purposes.

---
Video Explanation Here!!
https://youtu.be/GwmV8CSvPdU?si=9fMITg3Bhbydt_Kr

## 🔧 Features

- **Emergency Verification & Panic Detection**  
  Detects distress or panic from user input and responds with calm, reassuring language.
  
- **Location Detection**  
  Retrieves or simulates user location using mock GPS or manual input, focused on Iloilo City districts.
  
- **Nearby Hospital Finder**  
  Retrieves hospital data from a local database or falls back to web search if the location isn't found.
  
- **Ambulance Contact Simulation**  
  Attempts to contact a hospital ambulance with probabilistic success and provides alternatives if needed.

- **Human-Centered Design**  
  Speaks in calm, clear instructions; guides the user step-by-step in crisis scenarios.

---

## 🤖 How It Works

This agent is built using the `google.adk` framework and uses custom tools to perform emergency response actions:

### 1. `EmergencyVerificationTool`
- Detects panic based on keywords.
- Verifies whether the described situation is an emergency.
- Responds with calming messages if panic is detected.

### 2. `GetCurrentLocationTool`
- Simulates GPS-based location detection.
- Allows fallback manual input.
- Defaults to districts in **Iloilo City**.

### 3. `FindNearbyHospitalsTool`
- Uses a hardcoded dictionary of hospitals by district.
- Falls back to online search using `google_search()` if the location isn't matched.

### 4. `ContactAmbulanceTool`
- Simulates ambulance dispatch success based on emergency type.
- Includes fallback phone numbers: Red Cross (143), MMDA (136), Emergency (911).

---

## 🧠 Agent Instruction

The agent follows a defined **flow**:
1. Confirm if an emergency is happening.
2. Detect panic and respond appropriately.
3. Get the user's location.
4. Search for nearby hospitals.
5. Attempt ambulance contact (50–70% success rate).
6. Retry if failed; provide fallback numbers.
7. Stay with the user and offer guidance.

