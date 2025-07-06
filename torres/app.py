from flask import Flask, render_template, jsonify, request
import json
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = Flask(__name__)

def get_current_location_tool(lat, lng):
    """Tool to get the current location using coordinates"""
    try:
        geolocator = Nominatim(user_agent="emergency_ai_agent")
        location = geolocator.reverse((lat, lng))
        return {
            "success": True,
            "location": {
                "address": location.address,
                "latitude": lat,
                "longitude": lng
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def search_nearby_hospitals(lat, lng):
    """Search for nearby hospitals"""
    # In a real implementation, this would use Google Places API
    # For demo, returning mock data based on the location
    hospitals = [
        {"name": "City General Hospital", "distance": "2.1 km", "address": "123 Medical Ave"},
        {"name": "St. Luke's Medical Center", "distance": "3.4 km", "address": "456 Health St"},
        {"name": "Regional Medical Center", "distance": "4.2 km", "address": "789 Care Blvd"}
    ]
    return hospitals

def contact_ambulance_tool(emergency_details):
    """Tool to contact ambulance services (mock implementation)"""
    is_available = random.random() < 0.5
    
    if is_available:
        nearby_hospitals = search_nearby_hospitals(
            emergency_details.get('latitude'),
            emergency_details.get('longitude')
        )
        return {
            "success": True,
            "message": "Ambulance dispatched successfully",
            "eta": "10 minutes",
            "nearby_hospitals": nearby_hospitals
        }
    else:
        return {
            "success": False,
            "message": "All ambulances currently occupied. Trying alternative services..."
        }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/emergency', methods=['POST'])
def handle_emergency():
    try:
        data = request.json
        emergency_description = data.get('description', '')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Get location details
        location_result = get_current_location_tool(latitude, longitude)
        if not location_result["success"]:
            return jsonify({"error": "Unable to determine location"}), 400

        # Contact ambulance service
        ambulance_result = contact_ambulance_tool({
            'description': emergency_description,
            'latitude': latitude,
            'longitude': longitude
        })

        # Prepare response
        response = {
            "location": location_result["location"],
            "ambulance_status": ambulance_result["message"]
        }

        if ambulance_result["success"]:
            response.update({
                "eta": ambulance_result["eta"],
                "nearby_hospitals": ambulance_result["nearby_hospitals"]
            })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 