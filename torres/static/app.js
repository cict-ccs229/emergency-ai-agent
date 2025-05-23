async function requestHelp() {
    const description = document.getElementById('emergency-description').value;
    const statusContainer = document.getElementById('status-container');
    const locationStatus = document.getElementById('location-status');
    const ambulanceStatus = document.getElementById('ambulance-status');
    const hospitalsList = document.getElementById('hospitals-list');

    // Show status container
    statusContainer.style.display = 'block';
    locationStatus.textContent = 'Getting your location...';

    try {
        // Get user's location
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        });

        const { latitude, longitude } = position.coords;

        // Send emergency request
        const response = await fetch('/api/emergency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description,
                latitude,
                longitude
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Update location status
            locationStatus.textContent = `Location: ${data.location.address}`;

            // Update ambulance status
            ambulanceStatus.textContent = `Status: ${data.ambulance_status}`;

            // Display nearby hospitals if available
            if (data.nearby_hospitals) {
                hospitalsList.innerHTML = '<h3>Nearby Hospitals:</h3>';
                data.nearby_hospitals.forEach(hospital => {
                    const hospitalDiv = document.createElement('div');
                    hospitalDiv.className = 'hospital-item';
                    hospitalDiv.innerHTML = `
                        <strong>${hospital.name}</strong><br>
                        Distance: ${hospital.distance}<br>
                        Address: ${hospital.address}
                    `;
                    hospitalsList.appendChild(hospitalDiv);
                });
            }

            // Text-to-speech notification
            const message = `Emergency services have been notified. ${data.ambulance_status}`;
            const speech = new SpeechSynthesisUtterance(message);
            window.speechSynthesis.speak(speech);
        } else {
            throw new Error(data.error || 'Failed to process emergency request');
        }
    } catch (error) {
        console.error('Error:', error);
        ambulanceStatus.textContent = `Error: ${error.message}`;
    }
} 