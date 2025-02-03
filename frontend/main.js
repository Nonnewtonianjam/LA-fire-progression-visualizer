// Frontend setup using a basic JavaScript structure
console.log('Dashboard initialized');

// Initialize the map centered on LA area
const map = L.map('map').setView([34.0522, -118.2437], 9);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: ' OpenStreetMap contributors'
}).addTo(map);

// Store fire and AQI data
let fireData = [];
let aqiData = [];
let currentDateIndex = 0;
let animationInterval;

// Convert acres to meters for circle radius
function acresToMeters(acres) {
    // 1 acre = 4046.86 square meters
    // Area = π * r²
    // Therefore, r = sqrt(area/π)
    const squareMeters = acres * 4046.86;
    return Math.sqrt(squareMeters / Math.PI);
}

// Fetch data from backend
async function fetchData() {
    try {
        const response = await fetch('/api/fire_aqi_data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        if (data.status === 'success') {
            fireData = data.fire_data || [];
            aqiData = data.aqi_data || [];
            updateVisualization(new Date('2025-01-07'));
        } else {
            console.error('Error in data:', data.message);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Update visualization for a specific date
function updateVisualization(date) {
    // Clear existing markers
    map.eachLayer((layer) => {
        if (layer instanceof L.Circle) {
            map.removeLayer(layer);
        }
    });

    // Filter and display fire data for the selected date
    const dateStr = date.toISOString().split('T')[0];
    const currentFires = fireData.filter(fire => fire.date === dateStr);
    
    currentFires.forEach(fire => {
        const radius = acresToMeters(fire.size);
        const circle = L.circle([fire.latitude, fire.longitude], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: radius
        }).addTo(map);

        // Add a popup with fire information
        circle.bindPopup(`
            <strong>${fire.name}</strong><br>
            Size: ${fire.size.toLocaleString()} acres<br>
            Date: ${dateStr}
        `);
    });

    // Update fire details
    const totalAcres = currentFires.reduce((sum, fire) => sum + fire.size, 0);
    document.getElementById('fireDetails').innerHTML = `
        <p>Active Fires: ${currentFires.length}</p>
        <p>Total Area: ${totalAcres.toLocaleString()} acres</p>
        <p>Date: ${dateStr}</p>
    `;

    // Update AQI information
    const currentAQI = aqiData.find(aqi => aqi.date === dateStr);
    if (currentAQI) {
        document.getElementById('aqiDetails').innerHTML = `
            <p>AQI Level: ${currentAQI.value}</p>
            <p>Status: ${getAQIStatus(currentAQI.value)}</p>
        `;
    }
}

// Get AQI status text
function getAQIStatus(value) {
    if (value <= 50) return 'Good';
    if (value <= 100) return 'Moderate';
    if (value <= 150) return 'Unhealthy for Sensitive Groups';
    if (value <= 200) return 'Unhealthy';
    if (value <= 300) return 'Very Unhealthy';
    return 'Hazardous';
}

// Handle date selection
document.getElementById('dateSelector').addEventListener('change', (e) => {
    const selectedDate = new Date(e.target.value);
    updateVisualization(selectedDate);
});

// Handle animation playback
document.getElementById('playButton').addEventListener('click', () => {
    const button = document.getElementById('playButton');
    if (button.textContent === 'Play Animation') {
        button.textContent = 'Pause Animation';
        startAnimation();
    } else {
        button.textContent = 'Play Animation';
        stopAnimation();
    }
});

// Animation controls
function startAnimation() {
    if (animationInterval) return;
    
    animationInterval = setInterval(() => {
        const date = new Date('2025-01-07');
        date.setDate(date.getDate() + currentDateIndex);
        
        if (currentDateIndex >= 23) { // 23 days between Jan 7 and Jan 30
            currentDateIndex = 0;
            stopAnimation();
        } else {
            currentDateIndex++;
            updateVisualization(date);
            document.getElementById('dateSelector').value = date.toISOString().split('T')[0];
        }
    }, 1000); // Update every second
}

function stopAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
        document.getElementById('playButton').textContent = 'Play Animation';
    }
}

// Initialize the dashboard
fetchData();
