from google.adk.tools import BaseTool
import random

class GetCurrentLocationTool(BaseTool):
    """Tool to get the user's current GPS location."""
    
    def call(self, **kwargs) -> dict:
        # Simulating a GPS location retrieval
        # In a real application, this would interface with a GPS service or API
        location = {
            "latitude": random.uniform(10.0, 11.0),  # Simulated latitude
            "longitude": random.uniform(121.0, 122.0)  # Simulated longitude
        }
        return {"location": location}