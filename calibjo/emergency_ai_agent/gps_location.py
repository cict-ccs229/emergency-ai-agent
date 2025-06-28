import requests
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv


BASE_URL = "http://127.0.0.1:8000" 

load_dotenv()
API_KEY = os.environ.get("AGENT_API_KEY")
if not API_KEY:
    print("Error: AGENT_API_KEY environment variable not set.")
    print("Please set it: export AGENT_API_KEY='your_secret_test_api_key'")
    exit(1)

HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY # Include your API key here
}

# --- Test 1: Health Check ---
print("--- Testing /health endpoint ---")
health_url = f"{BASE_URL}/health"
try:
    health_response = requests.get(health_url)
    health_response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
    print(f"Health Check Status: {health_response.status_code}")
    print(f"Health Check Response: {health_response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Health Check Failed: {e}")
    exit(1)

print("\n--- Sending message to /predict endpoint ---")

# --- Payload for the /predict endpoint ---
# This matches the AgentInput Pydantic model in your main.py
payload = {
    "text": "Tell me about the USS Enterprise (CV-6) and show me pictures."
}

# --- Send message to /predict ---
predict_url = f"{BASE_URL}/predict"
try:
    response = requests.post(predict_url, headers=HEADERS, json=payload, timeout=120) # Added timeout
    response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

    print(f"Response Status: {response.status_code}")
    print("Full response:")
    print(json.dumps(response.json(), indent=2))

    # --- Optional: Further check the response_parts ---
    response_data = response.json()
    if 'response_parts' in response_data and isinstance(response_data['response_parts'], list):
        print("\n--- Parsed Response Parts ---")
        for i, part in enumerate(response_data['response_parts']):
            if part.get('type') == 'text':
                print(f"Part {i+1} (Text): {part.get('content')[:100]}...") # Print first 100 chars
            elif part.get('type') == 'image':
                print(f"Part {i+1} (Image URL): {part.get('url')}")
            else:
                print(f"Part {i+1} (Unknown Type): {part}")
    else:
        print("\nResponse does not contain expected 'response_parts' list.")

except requests.exceptions.Timeout:
    print("Request timed out after 120 seconds.")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API server. Is it running?")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")
except json.JSONDecodeError:
    print(f"Non-JSON response: {response.text}")
    