# 🚑 Ambulance AI Agent (Iloilo Emergency Assistant)

A **Gemini-powered voice-friendly emergency agent** built using Google ADK Web, designed to help users in **Iloilo City** request ambulance assistance, locate nearby hospitals, and receive real-time first aid tips.

Watch the demo 👉 [YouTube Video](https://youtu.be/YOzVfeHEiQM)

---

## 🧭 Usage

Users can speak or type natural emergency messages like:

- "I’m injured in **Molo**."
- "My friend collapsed in **Jaro**."
- "Send an ambulance to **La Paz**!"

### The Agent will:

1. Prompt the user to **confirm the emergency**.
2. **Detect or request** the user’s current location.
3. **Search for nearby hospitals** — either from a predefined list or via **Google Search**.
4. Attempt to **dispatch a mock ambulance** (50% approval rate).
5. Ask **“What injury has been sustained?”**
6. Use **real-time web search** to provide **first aid tips** while the ambulance is en route.

---

## 🌟 Key Features

- 📍 **Location Awareness**: Retrieves mock address (e.g., "Arevalo, Iloilo City").
- 🏥 **Nearby Hospital Search**: Uses both hardcoded areas and Google fallback.
- 🚑 **Ambulance Dispatch Simulation**: Provides randomized ETA on approval.
- 🩹 **First Aid Suggestions**: Searches the web for what to do based on injury.
- 🧠 **Shared State Memory**: Tracks user location, hospital results, and ambulance status.
- 🔒 **Strict Domain-Specific Scope**: Responds only to **medical emergencies** in **Iloilo City**.

