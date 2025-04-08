document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle the recommendation form submission
    const recommendationForm = document.getElementById('recommendation-form');
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', handleRecommendationFormSubmit);
        
        // Update range input values
        const rangeInputs = document.querySelectorAll('input[type="range"]');
        rangeInputs.forEach(input => {
            const valueDisplay = document.getElementById(`${input.id}-value`);
            if (valueDisplay) {
                // Set initial value
                valueDisplay.textContent = input.value;
                
                // Update on input change
                input.addEventListener('input', function() {
                    valueDisplay.textContent = this.value;
                });
            }
        });
    }
    
    // Handle reverse lookup form
    const reverseLookupForm = document.getElementById('reverse-lookup-form');
    if (reverseLookupForm) {
        loadCropOptions();
        reverseLookupForm.addEventListener('submit', handleReverseLookupFormSubmit);
    }
    
    // Handle crop encyclopedia filtering
    const cropFilter = document.getElementById('crop-filter');
    if (cropFilter) {
        loadCropEncyclopedia();
        cropFilter.addEventListener('input', filterCrops);
    }
});

// Handle recommendation form submission
function handleRecommendationFormSubmit(event) {
    event.preventDefault();
    
    // Show loading spinner
    const loadingSpinner = document.getElementById('loading-spinner');
    loadingSpinner.style.display = 'block';
    
    // Hide previous results
    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'none';
    
    // Get form data
    const formData = new FormData(event.target);
    
    // Send request to server
    fetch('/api/recommend', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            displayError(data.error);
        }
    })
    .catch(error => {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        displayError('An error occurred while processing your request. Please try again later.');
        console.error('Error:', error);
    });
}

// Display recommendation results
function displayResults(data) {
    const resultsSection = document.getElementById('results-section');
    const cropNameElement = document.getElementById('crop-name');
    const cropConfidenceElement = document.getElementById('crop-confidence');
    const cropDescriptionElement = document.getElementById('crop-description');
    
    console.log("Recommendation data:", data);
    
    // Set crop name
    cropNameElement.textContent = capitalizeFirstLetter(data.crop);
    
    // Set confidence if the element exists (might not be in all templates)
    if (cropConfidenceElement) {
        const confidence = data.confidence_scores[data.crop];
        // Ensure confidence is a valid number
        const confidenceValue = !isNaN(confidence) ? Math.round(confidence) : "N/A";
        cropConfidenceElement.textContent = `${confidenceValue}% Confidence`;
    }
    
    // Display the results section
    resultsSection.style.display = 'block';
    if (resultsSection.classList) {
        resultsSection.classList.add('fade-in');
    }
    
    // Get optimal conditions for the crop
    fetch(`/api/crop_conditions?crop=${data.crop}`)
        .then(response => response.json())
        .then(conditionsData => {
            if (conditionsData.success) {
                // Set crop description
                cropDescriptionElement.textContent = conditionsData.conditions.description || 
                    "A suitable crop for your soil conditions.";
                
                // Update parameter table
                updateParameterTable(data, conditionsData.conditions);
                
                // Create charts
                createConfidenceChart(data.confidence_scores);
                
                // Create parameter comparison chart if the function exists
                if (typeof createParameterComparisonChart === 'function') {
                    createParameterComparisonChart(data, conditionsData.conditions);
                }
            }
        })
        .catch(error => {
            console.error('Error getting crop conditions:', error);
            // Still show the chart even if we can't get conditions
            createConfidenceChart(data.confidence_scores);
        });
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Update parameter table with user values and optimal ranges
function updateParameterTable(data, conditions) {
    const parameterTable = document.getElementById('parameter-table');
    const formData = new FormData(document.getElementById('recommendation-form'));
    
    // Clear previous content
    parameterTable.innerHTML = '';
    
    // Define parameters to display
    const parameters = [
        { id: 'nitrogen', name: 'Nitrogen (N)', unit: 'kg/ha', min: 'n_min', max: 'n_max' },
        { id: 'phosphorus', name: 'Phosphorus (P)', unit: 'kg/ha', min: 'p_min', max: 'p_max' },
        { id: 'potassium', name: 'Potassium (K)', unit: 'kg/ha', min: 'k_min', max: 'k_max' },
        { id: 'temperature', name: 'Temperature', unit: '°C', min: 'temperature_min', max: 'temperature_max' },
        { id: 'humidity', name: 'Humidity', unit: '%', min: 'humidity_min', max: 'humidity_max' },
        { id: 'ph', name: 'pH', unit: '', min: 'ph_min', max: 'ph_max' },
        { id: 'rainfall', name: 'Rainfall', unit: 'mm', min: 'rainfall_min', max: 'rainfall_max' }
    ];
    
    // Create rows for each parameter
    parameters.forEach(param => {
        const value = formData.get(param.id);
        const row = document.createElement('div');
        row.className = 'parameter-row';
        
        const parameterName = document.createElement('div');
        parameterName.className = 'parameter-name';
        parameterName.textContent = param.name;
        
        const parameterValue = document.createElement('div');
        parameterValue.className = 'parameter-value';
        
        const valueSpan = document.createElement('span');
        valueSpan.textContent = `${value} ${param.unit}`;
        
        const optimalRange = document.createElement('div');
        optimalRange.className = 'optimal-range';
        optimalRange.textContent = `Optimal: ${conditions[param.min]} - ${conditions[param.max]} ${param.unit}`;
        
        parameterValue.appendChild(valueSpan);
        parameterValue.appendChild(optimalRange);
        
        row.appendChild(parameterName);
        row.appendChild(parameterValue);
        
        parameterTable.appendChild(row);
    });
}

// Display error message
function displayError(message) {
    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-danger alert-dismissible fade show';
    errorAlert.setAttribute('role', 'alert');
    errorAlert.innerHTML = `
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const formContainer = document.querySelector('.input-section');
    formContainer.insertBefore(errorAlert, formContainer.firstChild);
    
    // Automatically dismiss after 5 seconds
    setTimeout(() => {
        errorAlert.classList.remove('show');
        setTimeout(() => {
            errorAlert.remove();
        }, 300);
    }, 5000);
}

// Load crop options for reverse lookup
function loadCropOptions() {
    const cropSelect = document.getElementById('crop-select');
    if (cropSelect) {
        fetch('/api/crops')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Sort crops alphabetically
                    const crops = data.crops.sort();
                    
                    // Add options to select element
                    crops.forEach(crop => {
                        const option = document.createElement('option');
                        option.value = crop;
                        option.textContent = capitalizeFirstLetter(crop);
                        cropSelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error loading crops:', error);
            });
    }
}

// Handle reverse lookup form submission
function handleReverseLookupFormSubmit(event) {
    event.preventDefault();
    
    const cropSelect = document.getElementById('crop-select');
    const selectedCrop = cropSelect.value;
    
    if (!selectedCrop) {
        displayError('Please select a crop');
        return;
    }
    
    // Show loading spinner
    const loadingSpinner = document.getElementById('reverse-loading-spinner');
    loadingSpinner.style.display = 'block';
    
    // Hide previous results
    const conditionsSection = document.getElementById('conditions-section');
    conditionsSection.style.display = 'none';
    
    // Get crop conditions
    fetch(`/api/crop_conditions?crop=${selectedCrop}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            if (data.success) {
                displayCropConditions(selectedCrop, data.conditions);
            } else {
                displayError(data.error);
            }
        })
        .catch(error => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            displayError('An error occurred while processing your request. Please try again later.');
            console.error('Error:', error);
        });
}

// Display crop conditions for reverse lookup
function displayCropConditions(cropName, conditions) {
    const conditionsSection = document.getElementById('conditions-section');
    const cropNameElement = document.getElementById('conditions-crop-name');
    const cropDescriptionElement = document.getElementById('conditions-crop-description');
    const conditionsTable = document.getElementById('conditions-table');
    
    // Set crop name and description
    cropNameElement.textContent = capitalizeFirstLetter(cropName);
    cropDescriptionElement.textContent = conditions.description;
    
    // Clear previous content
    conditionsTable.innerHTML = '';
    
    // Define parameters to display
    const parameters = [
        { name: 'Nitrogen (N)', unit: 'kg/ha', min: 'n_min', max: 'n_max' },
        { name: 'Phosphorus (P)', unit: 'kg/ha', min: 'p_min', max: 'p_max' },
        { name: 'Potassium (K)', unit: 'kg/ha', min: 'k_min', max: 'k_max' },
        { name: 'Temperature', unit: '°C', min: 'temperature_min', max: 'temperature_max' },
        { name: 'Humidity', unit: '%', min: 'humidity_min', max: 'humidity_max' },
        { name: 'pH', unit: '', min: 'ph_min', max: 'ph_max' },
        { name: 'Rainfall', unit: 'mm', min: 'rainfall_min', max: 'rainfall_max' }
    ];
    
    // Create rows for each parameter
    parameters.forEach(param => {
        const row = document.createElement('tr');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = param.name;
        
        const rangeCell = document.createElement('td');
        rangeCell.innerHTML = `${conditions[param.min]} - ${conditions[param.max]} <span class="text-muted">${param.unit}</span>`;
        
        row.appendChild(nameCell);
        row.appendChild(rangeCell);
        
        conditionsTable.appendChild(row);
    });
    
    // Display the conditions section
    conditionsSection.style.display = 'block';
    conditionsSection.classList.add('fade-in');
    
    // Create parameter chart
    createRangeChart(cropName, conditions);
    
    // Scroll to results
    conditionsSection.scrollIntoView({ behavior: 'smooth' });
}

// Load crop encyclopedia data
function loadCropEncyclopedia() {
    const cropGrid = document.getElementById('crop-grid');
    
    fetch('/api/crops')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Sort crops alphabetically
                const crops = data.crops.sort();
                
                // Create crop cards
                crops.forEach((crop, index) => {
                    fetch(`/api/crop_conditions?crop=${crop}`)
                        .then(response => response.json())
                        .then(conditionsData => {
                            if (conditionsData.success) {
                                const cropCard = createCropCard(crop, conditionsData.conditions, index);
                                cropGrid.appendChild(cropCard);
                            }
                        });
                });
            }
        })
        .catch(error => {
            console.error('Error loading crops:', error);
        });
}

// Create a crop card for the encyclopedia
function createCropCard(cropName, conditions, index) {
    // Define a set of background images to cycle through
    const cropImages = [
        'https://images.unsplash.com/photo-1583602096973-37ca0307326d',
        'https://images.unsplash.com/photo-1528839390497-a161db4bac71',
        'https://images.unsplash.com/photo-1516234137022-7d61576807db',
        'https://images.unsplash.com/photo-1530267981375-f0de937f5f13',
        'https://images.unsplash.com/photo-1527762031550-522c5d9240fd',
        'https://images.unsplash.com/photo-1534940519139-f860fb3c6e38'
    ];
    
    // Get an image based on the index (cycle through the available images)
    const imageUrl = cropImages[index % cropImages.length];
    
    const colDiv = document.createElement('div');
    colDiv.className = 'col-md-4 mb-4';
    
    colDiv.innerHTML = `
        <div class="card crop-card" data-crop="${cropName}">
            <img src="${imageUrl}" class="card-img-top crop-card-img" alt="${capitalizeFirstLetter(cropName)}">
            <div class="card-body">
                <h5 class="card-title crop-card-title">${capitalizeFirstLetter(cropName)}</h5>
                <p class="card-text">${conditions.description.substring(0, 100)}...</p>
                <div class="d-flex justify-content-between">
                    <span class="text-primary">
                        <i class="fas fa-temperature-high me-1"></i> ${conditions.temperature_min}-${conditions.temperature_max}°C
                    </span>
                    <span class="text-primary">
                        <i class="fas fa-tint me-1"></i> ${conditions.rainfall_min}-${conditions.rainfall_max} mm
                    </span>
                </div>
                <button class="btn btn-sm btn-outline-primary mt-3 w-100">View Details</button>
            </div>
        </div>
    `;
    
    // Add click event to the button
    const button = colDiv.querySelector('button');
    button.addEventListener('click', () => {
        window.location.href = `/reverse_lookup?crop=${cropName}`;
    });
    
    return colDiv;
}

// Filter crops in the encyclopedia
function filterCrops() {
    const filterText = document.getElementById('crop-filter').value.toLowerCase();
    const cropCards = document.querySelectorAll('.crop-card');
    
    cropCards.forEach(card => {
        const cropName = card.getAttribute('data-crop');
        if (cropName.includes(filterText)) {
            card.parentElement.style.display = 'block';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}

// Helper function to capitalize the first letter of each word
function capitalizeFirstLetter(string) {
    return string.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}
