# Emergency Ambulance Dispatch Agent

This project simulates an emergency ambulance dispatch system using a conversational Python agent. The agent confirms accidents, retrieves the user's location (without displaying coordinates), and iterates through nearby hospitals until an ambulance dispatch is approved. If no dispatch is approved, a fallback message is shown with a contact number.

**▶️ [Watch a video explanation here](https://youtu.be/Og8WAvAxcmk)**

---

## Features

- **Accident Confirmation:**  
  The agent first asks the user to confirm whether an accident has occurred before proceeding.

- **Location Retrieval:**  
  Uses a mock tool (`GetCurrentLocationTool`) to retrieve the user's GPS coordinates (not shown to the user).

- **Hospital Search & Dispatch:**  
  - Uses a `google_search` tool to obtain nearby hospitals.
  - Attempts to dispatch an ambulance via the `ContactAmbulanceTool` (50% simulated approval rate).
  - If denied, prompts the user to try the next hospital.
  - If approved, outputs the hospital name and estimated arrival time.
  - If no hospital approves, provides a fallback message with a contact number.

- **Conversational Agent:**  
  The agent can also respond to chat requests for ambulance dispatch.

---

## Setup

### Prerequisites

1. **Python Installation**
   - Install Python 3.8 or later (Python 3.12 recommended).
   - [Download Python here](https://www.python.org/downloads/).

2. **Gemini API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Sign in with your Google account.
   - Create and copy your Gemini API key.

3. **Project Files**
   - Clone this repository or download the project files to your local machine.

4. **Environment Variables**
   - In the project directory, create a `.env` file with the following content:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=FALSE
     GOOGLE_GENAI_USE_GEMINI=TRUE
     GOOGLE_API_KEY=YOUR_GEMINI_API_KEY_HERE
     ```
     Replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key.

5. **Install Dependencies**
   - Open a terminal in the project directory and run:
     ```bash
     pip install -r requirements.txt
     ```

---

### Agent Development Kit (ADK) Setup

1. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install the Agent Development Kit and dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the ADK installation:**
   ```bash
   adk --help
   ```

4. **Set up your `.env` file** as described above.

5. **Run the agent:**
   ```bash
   adk web
   ```

> **Note:** You do **not** need to set up Vertex AI or a Google Cloud project for Gemini API key usage.

---

## Usage

1. **Run the agent:**
   ```bash
   adk web
   ```

2. **Follow the prompts:**
   - Confirm whether the accident has occurred.
   - The agent will retrieve your location (coordinates are not shown).
   - The system will search for nearby hospitals and attempt to dispatch an ambulance.
   - If denied, you will be prompted to try another hospital.
   - If no hospital approves, a fallback message is shown with a contact number.

---

## Project Structure

- **agent.py:**  
  Main logic for accident confirmation, location retrieval, hospital search, and ambulance dispatch attempts.

- **ambulance_tools.py:**  
  - `GetCurrentLocationTool`: Mocks retrieval of the user’s GPS coordinates.
  - `ContactAmbulanceTool`: Mocks contacting the ambulance service with a simulated approval.

- **requirements.txt:**  
  Lists all Python packages required to run the project.

---

## Notes

- This is a mock simulation; no real ambulance service is contacted.
- The `google_search` tool is expected to return a list of hospital names.
- The agent uses the Gemini API via your API key from Google AI Studio.
- **No Vertex AI or Google Cloud project setup is required.**

---

## Contact

For more information or assistance, please contact the project maintainer.