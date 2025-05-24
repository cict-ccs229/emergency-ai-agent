# Emergency AI Agent for Iloilo City

This project is an AI-powered voice-activated emergency assistant designed to help users in Iloilo City, Philippines, by providing quick access to ambulance dispatch services and information about nearby hospitals.

Video Demo: https://drive.google.com/drive/folders/1UwQgmwK8QrdHTuWDxgc3a3TVlj_FcGCO?usp=drive_link

---

## Features

- **Voice-enabled emergency assistant** using text-to-speech (TTS) for responses.
- **Location detection** based on public IP address to approximate user location.
- **Nearby hospital listing** specific to Iloilo City.
- **Ambulance dispatch simulation** by contacting hospitals and confirming ambulance availability.
- **Conversational flow** that confirms emergencies before dispatching ambulances.
- Handles **API rate limiting** and retries gracefully.

---

## How It Works

1. When a user requests emergency assistance, the agent asks for confirmation before proceeding.
2. If confirmed, it retrieves the user’s approximate location via IP geolocation.
3. The agent lists nearby hospitals in Iloilo City.
4. It attempts to contact hospitals to dispatch an ambulance and informs the user about ambulance status and ETA.
5. If ambulances are unavailable or location is unknown, it responds accordingly.
6. The agent also handles queries about nearby hospitals without dispatching ambulances.
7. Non-emergency queries are politely declined.

---

## Requirements

- Python 3.8+
- Packages: `requests`, `pyttsx3`, `asyncio`
- Internet connection for IP geolocation and API calls.

---

## Setup and Running

1. Clone or download the repository.
2. Install required packages:

   ```bash
   pip install requests pyttsx3

## Interact with the agent via the console input. Type emergency-related commands like:

"Help"

"I need an ambulance"

"Send help"

"What hospitals are near me?"



