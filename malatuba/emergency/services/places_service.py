import os
import requests
from typing import Dict, List, Any


class PlacesService:
    """Handles resolving text queries to location details using Google Places API."""

    def __init__(self):
        self.places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    def find_place_from_text(self, query: str) -> Dict[str, Any]:
        if not self.places_api_key:
            return {"error": "Missing Google Places API key."}

        endpoint = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": query,
            "inputtype": "textquery",
            "fields": "place_id,formatted_address,name,photos,geometry",
            "key": self.places_api_key,
        }

        try:
            res = requests.get(endpoint, params=params)
            res.raise_for_status()
            candidates = res.json().get("candidates", [])
            if not candidates:
                return {"error": "No places found."}

            details = candidates[0]
            return {
                "place_id": details["place_id"],
                "place_name": details["name"],
                "place_address": details["formatted_address"],
                "photos": self._photo_urls(details.get("photos", [])),
                "map_url": f"https://www.google.com/maps/place/?q=place_id:{details['place_id']}",
                "lat": str(details["geometry"]["location"]["lat"]),
                "lng": str(details["geometry"]["location"]["lng"]),
            }

        except requests.RequestException as e:
            return {"error": str(e)}

    def _photo_urls(self, photos: List[Dict[str, Any]], maxwidth: int = 400) -> List[str]:
        base_url = "https://maps.googleapis.com/maps/api/place/photo"
        return [
            f"{base_url}?maxwidth={maxwidth}&photoreference={p['photo_reference']}&key={self.places_api_key}"
            for p in photos
        ]
