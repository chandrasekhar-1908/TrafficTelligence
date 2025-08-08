document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded");
    
    // Update current time
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }
    
    updateTime();
    setInterval(updateTime, 1000);
    
    // Handle form submission
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        console.log("Form found");
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("Form submitted");
            
            // Show loading state
            const btnSubmit = document.querySelector('.btn-predict');
            const originalText = btnSubmit.innerHTML;
            btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            btnSubmit.disabled = true;
            
            // Collect form data
            const formData = new FormData(predictionForm);
            console.log("Form data collected");
            
            // Send prediction request
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                console.log("Response received:", response);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Data received:", data);
                
                // Update prediction result
                const predictionValue = document.getElementById('prediction-value');
                if (predictionValue) {
                    predictionValue.textContent = data.prediction;
                } else {
                    console.error("prediction-value element not found");
                }
                
                // Update status with color
                const statusElement = document.getElementById('prediction-status');
                if (statusElement) {
                    statusElement.textContent = data.status;
                    statusElement.style.backgroundColor = getStatusColor(data.status_color);
                    statusElement.style.color = 'white';
                } else {
                    console.error("prediction-status element not found");
                }
                
                // Update traffic visualization
                updateTrafficVisualization(data.prediction, data.status);
                
                // Reset button
                btnSubmit.innerHTML = originalText;
                btnSubmit.disabled = false;
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Reset button on error
                btnSubmit.innerHTML = originalText;
                btnSubmit.disabled = false;
                
                // Show error message
                alert('An error occurred while processing your request. Please try again.');
            });
        });
    } else {
        console.error("Form not found");
    }
    
    // Get status color
    function getStatusColor(colorName) {
        switch(colorName) {
            case 'green': return '#27ae60';
            case 'yellow': return '#f1c40f';
            case 'red': return '#e74c3c';
            default: return '#95a5a6';
        }
    }
    
    // Update traffic visualization based on prediction
    function updateTrafficVisualization(prediction, status) {
        console.log("Updating traffic visualization with prediction:", prediction, "status:", status);
        
        // Update status bar
        const statusFill = document.getElementById('status-fill');
        if (statusFill) {
            const percentage = Math.min(100, Math.max(0, prediction / 3)); // Scale prediction to percentage
            statusFill.style.width = percentage + '%';
        } else {
            console.error("status-fill element not found");
        }
        
        // Update status text
        const statusText = document.getElementById('status-text');
        if (statusText) {
            statusText.textContent = status;
        } else {
            console.error("status-text element not found");
        }
        
        // Update traffic details
        let avgSpeed, congestionLevel, travelTime;
        
        if (prediction < 100) {
            avgSpeed = '65 mph';
            congestionLevel = 'Low';
            travelTime = '15 min';
        } else if (prediction < 200) {
            avgSpeed = '45 mph';
            congestionLevel = 'Moderate';
            travelTime = '25 min';
        } else {
            avgSpeed = '25 mph';
            congestionLevel = 'High';
            travelTime = '45 min';
        }
        
        const avgSpeedElement = document.getElementById('avg-speed');
        if (avgSpeedElement) {
            avgSpeedElement.textContent = avgSpeed;
        } else {
            console.error("avg-speed element not found");
        }
        
        const congestionLevelElement = document.getElementById('congestion-level');
        if (congestionLevelElement) {
            congestionLevelElement.textContent = congestionLevel;
        } else {
            console.error("congestion-level element not found");
        }
        
        const travelTimeElement = document.getElementById('travel-time');
        if (travelTimeElement) {
            travelTimeElement.textContent = travelTime;
        } else {
            console.error("travel-time element not found");
        }
        
        // Change traffic image based on status
        const trafficImage = document.querySelector('.camera-feed img');
        if (trafficImage) {
            if (prediction < 100) {
                trafficImage.src = "https://images.unsplash.com/photo-1474931193364-3cc6d7f1e1c3?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";
            } else if (prediction < 200) {
                trafficImage.src = "https://images.unsplash.com/photo-1589122374633-3a562e00e6b6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";
            } else {
                trafficImage.src = "https://images.unsplash.com/photo-1591189052958-8d0b9a6c6d6f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80";
            }
        } else {
            console.error("traffic image not found");
        }
    }
    
    // Set default values for current time
    const now = new Date();
    const hourElement = document.getElementById('hour');
    const dayOfWeekElement = document.getElementById('day_of_week');
    const monthElement = document.getElementById('month');
    
    if (hourElement) hourElement.value = now.getHours();
    if (dayOfWeekElement) dayOfWeekElement.value = now.getDay();
    if (monthElement) monthElement.value = now.getMonth() + 1;
    
    console.log("Default values set");
});