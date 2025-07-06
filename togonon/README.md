# Emergency Ambulance Support AI Agent (Philippines)

This project implements an AI agent using the Google Agent Development Kit (ADK) designed to assist users in the Philippines with contacting local ambulance services during medical emergencies.

## Problem Addressed

In the Philippines, accessing emergency ambulance services can be challenging due to:
- Lack of a centralized, reliable emergency response system.
- Panic attacks hindering clear communication and decision-making.
- Occasional reliance on social media when official channels fail.

This AI agent aims to reduce the time and complexity involved in contacting help.

## Features

- **Guided Emergency Interaction**: Helps users articulate their emergency.
- **Location Assistance**: Can simulate fetching the user's current location in Iloilo City.
- **Hospital Search**: Can search for nearby hospitals 
- **Mock Ambulance Contact**: Simulates contacting ambulance services for a chosen hospital with a 50% success rate.
- **API Key Management**: Uses a `.env` file to store API keys, loaded via `python-dotenv`.

## Project Structure

- `togonon/`
  - `README.md`: This file.
  - `ai_agent/`
    - `__init__.py`: Marks `ai_agent` as a Python package and should contain `from . import agent`.
    - `agent.py`: Contains the agent definition and custom tool class definitions.
    - `requirements.txt`: Python package dependencies for the agent.
    - `.env`: Stores API keys.

## Setup

1.  **Prerequisites**:
    *   Ensure you have Python installed.
    *   It is highly recommended to use a Python virtual environment for this project.

2.  **Create `.env` file**:
    *   Navigate to the `togonon/ai_agent/` directory.
    *   Create a file named `.env`.
    *   Add your API keys to this file. For example:
        ```
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_API_KEY"
        ```
    *   Ensure your `.gitignore` file (ideally at the project root or within `ai_agent`) lists `.env`.
3.  **Install Dependencies**:
    *   Navigate to the `togonon/ai_agent/` directory in your terminal.
    *   If using a virtual environment, ensure it's activated.
    *   Run:
        ```bash
        pip install -r requirements.txt
        ```

## Running the Agent

1.  **Navigate to the agent package directory**:
    ```bash
    cd path/to/your/project/togonon/ai_agent
    ```
2.  **Run `adk web`**:
    adk web
    
3.  Open the URL provided by `adk web` (usually `http://localhost:8000`) in your browser and go to the `/dev-ui` path to interact with the agent.

Alternatively, for a simple command-line simulation of tool calls (without the interactive ADK web UI):
```bash
cd path/to/your/project/togonon/ai_agent
python agent.py
``` 