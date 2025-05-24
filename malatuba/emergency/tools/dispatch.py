# dispatch.py
import random
import math
from emergency.services.places_service import PlacesService


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lng points using Haversine formula."""
    R = 6371  # Earth radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def dispatch_ambulance(user_query: str) -> dict:
    """
    Simulate ambulance dispatch from a hospital to user's location.
    Uses a hardcoded list of hospitals (mock nearby).
    Tries each hospital until one succeeds (50% chance).
    """
    service = PlacesService()
    user_location = service.find_place_from_text(user_query)

    if "error" in user_location:
        return {"error": "Failed to resolve user location."}

    # Hardcoded mock nearby hospitals
    nearby_hospitals = [
        "City Hospital",
        "General Medical Center",
        "Saint Mary's Hospital",
        "Downtown Clinic",
        "Mercy Health Center",
    ]

    for hospital_name in nearby_hospitals:
        if random.random() > 0.5:  # 50% chance hospital can dispatch ambulance
            hospital_location = service.find_place_from_text(hospital_name)
            if "error" in hospital_location:
                continue

            eta = int(haversine_distance(
                float(user_location["lat"]), float(user_location["lng"]),
                float(hospital_location["lat"]), float(hospital_location["lng"])
            ) / 0.6)  # Assuming average speed 60 km/h (1 km/min)

            return {
                "status": "ambulance dispatched",
                "ambulance_id": f"AMB-{random.randint(100, 999)}",
                "hospital": hospital_location["place_name"],
                "hospital_address": hospital_location["place_address"],
                "destination": user_location["place_name"],
                "destination_address": user_location["place_address"],
                "map_url": user_location["map_url"],
                "eta_minutes": eta
            }

    return {"error": "No available hospitals could dispatch an ambulance."}
