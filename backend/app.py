# Backend server setup using Flask
from flask import Flask, jsonify, send_from_directory
import requests
from datetime import datetime, timedelta
import logging
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Set up logging
logging.basicConfig(level=logging.INFO)

# Constants for API endpoints
NASA_FIRMS_API_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
EPA_AQI_API_URL = "https://aqs.epa.gov/data/api/dailyData/byState"

# Add your API keys here - these need to be replaced with valid keys
NASA_API_KEY = 'your_nasa_api_key'
EPA_API_KEY = 'your_epa_api_key'

# Mock data for fires (sizes in acres)
FIRES = [
    {
        "name": "Palisades Fire",
        "coordinates": [
            {"date": "2025-01-07", "latitude": 34.0522, "longitude": -118.5536, "size": 1200},
            {"date": "2025-01-08", "latitude": 34.0530, "longitude": -118.5540, "size": 3500},
            {"date": "2025-01-09", "latitude": 34.0535, "longitude": -118.5545, "size": 5000},
            {"date": "2025-01-10", "latitude": 34.0540, "longitude": -118.5550, "size": 6800},
            {"date": "2025-01-11", "latitude": 34.0545, "longitude": -118.5555, "size": 7500},
            {"date": "2025-01-12", "latitude": 34.0550, "longitude": -118.5560, "size": 8200}
        ]
    },
    {
        "name": "Eaton Fire",
        "coordinates": [
            {"date": "2025-01-09", "latitude": 34.2468, "longitude": -118.3029, "size": 800},
            {"date": "2025-01-10", "latitude": 34.2472, "longitude": -118.3035, "size": 2500},
            {"date": "2025-01-11", "latitude": 34.2480, "longitude": -118.3040, "size": 4200},
            {"date": "2025-01-12", "latitude": 34.2485, "longitude": -118.3045, "size": 5800},
            {"date": "2025-01-13", "latitude": 34.2490, "longitude": -118.3050, "size": 6500},
            {"date": "2025-01-14", "latitude": 34.2495, "longitude": -118.3055, "size": 7200}
        ]
    },
    {
        "name": "Hughes Fire",
        "coordinates": [
            {"date": "2025-01-10", "latitude": 34.4897, "longitude": -118.5259, "size": 1500},
            {"date": "2025-01-11", "latitude": 34.4900, "longitude": -118.5265, "size": 3000},
            {"date": "2025-01-12", "latitude": 34.4905, "longitude": -118.5270, "size": 4500},
            {"date": "2025-01-13", "latitude": 34.4910, "longitude": -118.5275, "size": 5800},
            {"date": "2025-01-14", "latitude": 34.4915, "longitude": -118.5280, "size": 6500},
            {"date": "2025-01-15", "latitude": 34.4920, "longitude": -118.5285, "size": 7500}
        ]
    }
]

# Mock AQI data
def generate_aqi_data():
    aqi_data = []
    start_date = datetime(2025, 1, 7)
    
    for i in range(24):  # 24 days from Jan 7 to Jan 30
        current_date = start_date + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Base AQI value that varies between 50-150
        base_aqi = 50 + (i % 5) * 25
        
        # Add higher AQI values near active fires
        active_fires = 0
        for fire in FIRES:
            for coord in fire["coordinates"]:
                if coord["date"] == date_str:
                    base_aqi += 75  # Larger AQI impact due to bigger fires
                    active_fires += 1
        
        # Multiply effect if multiple fires are active
        if active_fires > 1:
            base_aqi *= (1 + (active_fires - 1) * 0.5)
        
        aqi_data.append({
            "date": date_str,
            "value": min(int(base_aqi), 500),  # Cap at 500, using realistic AQI scale
            "latitude": 34.0522,  # LA center
            "longitude": -118.2437
        })
    
    return aqi_data

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/api/fire_aqi_data')
def get_fire_aqi_data():
    """Endpoint to get both fire and AQI data"""
    try:
        # Process fire data into a flat list
        fire_data = []
        for fire in FIRES:
            for coord in fire["coordinates"]:
                fire_data.append({
                    "name": fire["name"],
                    "date": coord["date"],
                    "latitude": coord["latitude"],
                    "longitude": coord["longitude"],
                    "size": coord["size"]  # Size in acres
                })
        
        aqi_data = generate_aqi_data()
        
        return jsonify({
            'fire_data': fire_data,
            'aqi_data': aqi_data,
            'status': 'success'
        })
    except Exception as e:
        logging.error(f"Error in get_fire_aqi_data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
