# LA Fire Dashboard

An interactive web application for visualizing fire progression and air quality data in the Los Angeles area. The dashboard tracks three major fires (Palisades, Eaton, and Hughes) from January 7-30, 2025, alongside their impact on air quality.

![Screenshot 2025-02-02 210524](https://github.com/user-attachments/assets/123019f6-1c49-4ba6-8d79-a5303582c0a2)



## Features

- **Interactive Map Visualization**
  - Real-time display of fire locations and sizes
  - Fire progression animation
  - Popup information for each fire showing acreage and dates
  - Circle sizes proportional to actual fire coverage

- **Time-Based Controls**
  - Date selector for specific day views
  - Animation playback controls
  - Sequential visualization of fire progression

- **Data Metrics**
  - Active fire count
  - Total area burned
  - Real-time Air Quality Index (AQI) levels
  - AQI status indicators

## Technical Stack

### Backend
- Flask (Python web framework)
- RESTful API endpoints
- Mock data generation for fires and AQI

### Frontend
- HTML5/CSS3
- JavaScript (ES6+)
- Leaflet.js for map visualization
- OpenStreetMap for base map tiles

## Project Structure

```
LAFire/
├── backend/
│   └── app.py           # Flask server and data endpoints
├── frontend/
│   ├── index.html       # Main HTML structure
│   ├── style.css        # CSS styling
│   └── main.js          # Frontend JavaScript
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd LAFire
```

2. Install Python dependencies:
```bash
pip install flask
```

3. Start the Flask server:
```bash
python backend/app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## Data Sources

The application currently uses mock data that simulates:
- Three major fires in the LA area (Palisades, Eaton, and Hughes)
- Combined burned area of over 22,900 acres
- Air Quality Index (AQI) data with fire impact correlation

## Usage

1. **View Fire Data**:
   - Fire locations are shown as red circles on the map
   - Circle sizes are proportional to the acres burned
   - Click on a fire circle to view detailed information

2. **Time Controls**:
   - Use the date selector to view specific days
   - Click "Play Animation" to see fire progression over time
   - Animation updates every second

3. **Monitor Air Quality**:
   - View real-time AQI levels
   - AQI status indicates air quality from "Good" to "Hazardous"
   - AQI calculations factor in multiple active fires


## License

This project is licensed under the MIT License - see the LICENSE file for details.
