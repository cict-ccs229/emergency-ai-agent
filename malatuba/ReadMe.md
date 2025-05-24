# 🚑 Emergency Dispatch Agent System

This project implements an AI-based emergency dispatch system. It leverages Google Maps to resolve user locations, simulates nearby hospital availability, and dispatches ambulances accordingly.

video link: https://youtu.be/lULiwoLxLK4

## 🧠 Project Overview

This system consists of a root agent and sub-agents to simulate emergency handling:

- **root_agent**: Entry point for user interaction.
- **ambulance_dispatch_agent**: Handles ambulance-related requests.
- **PlacesService**: Resolves free-text location queries using the Google Places API.
- **Dispatch Logic**: 
  - Uses a mock list of hospitals.
  - Randomly checks if each hospital can dispatch an ambulance (50% success rate).
  - Calculates ETA using Haversine distance formula.

---

## 🚀 How It Works

1. **User provides a location** (e.g., "123 Main St" or "near City Park").
2. **`PlacesService`** resolves the location.
3. **Nearby hospitals** are mocked as a fixed list.
4. Each hospital is **pinged (mocked)** — if available, ambulance is dispatched.
5. **ETA** is computed based on distance and average ambulance speed.
6. Returns dispatch confirmation, hospital info, and Google Maps link.

---

## 📁 Key Files

| File | Description |
|------|-------------|
| `agent.py` | Initializes the root agent and registers sub-agents |
| `ambulance_dispatch_agent.py` | Defines the ambulance dispatch logic and tool |
| `dispatch.py` | Core logic for hospital checking and ETA calculation |
| `places_service.py` | Wrapper for Google Places API to resolve locations |

---

