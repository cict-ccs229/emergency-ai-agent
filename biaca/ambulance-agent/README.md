# Emergency Ambulance Dispatch Agent

This project implements an AI agent designed to assist users in contacting local ambulance services during emergencies in the Philippines. The agent aims to streamline the process of requesting ambulance support, reducing the time and complexity involved in emergency situations.

## Features

- **Emergency Verification:**  
  The agent verifies the nature of the emergency through user interaction.

- **Location Retrieval:**  
  Utilizes a tool to obtain the user's current GPS coordinates (without displaying them).

- **Hospital Search:**  
  Searches for nearby hospitals using a web search tool.

- **Ambulance Contact:**  
  Attempts to contact the ambulance service with a simulated approval rate of 50%. If approved, it provides details about the dispatch.

## Setup Instructions

### Prerequisites

1. **Python Installation**  
   Ensure Python 3.8 or later is installed on your machine.

2. **Google ADK Installation**  
   Install the Google Agent Development Kit (ADK) by following the official documentation.

3. **Environment Variables**  
   Create a `.env` file in the project directory with the following content:
   ```
   GOOGLE_API_KEY=YOUR_API_KEY_HERE
   ```

### Installation

1. Clone the repository or download the project files to your local machine.

2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

### Running the Agent

To start the agent, run the following command in your terminal:
```
adk web
```

### Usage

1. Upon running the agent, follow the prompts to confirm the emergency situation.
2. The agent will retrieve your location and search for nearby hospitals.
3. It will attempt to contact the ambulance service and provide feedback on the dispatch status.

## Project Structure

- **main.py:**  
  Contains the complete implementation of the AI agent, including tool definitions and agent setup.

- **.gitignore:**  
  Specifies files and directories to be ignored by version control.

- **.env:**  
  Stores environment variables required for the application.

## Notes

- This project is a simulation and does not contact real ambulance services.
- Ensure to replace `YOUR_API_KEY_HERE` in the `.env` file with your actual API key.

## Contact

For further information or assistance, please reach out to the project maintainer.