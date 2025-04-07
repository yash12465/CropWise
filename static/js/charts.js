// Create a chart showing confidence scores for different crops
function createConfidenceChart(confidenceScores) {
    const ctx = document.getElementById('confidence-chart').getContext('2d');
    
    // Convert confidence scores object to arrays for the chart
    const crops = Object.keys(confidenceScores).map(crop => capitalizeFirstLetter(crop));
    const scores = Object.values(confidenceScores);
    
    // Sort by score (descending)
    const combinedData = crops.map((crop, i) => ({ crop, score: scores[i] }));
    combinedData.sort((a, b) => b.score - a.score);
    
    // Get top 5 crops
    const top5Crops = combinedData.slice(0, 5).map(item => item.crop);
    const top5Scores = combinedData.slice(0, 5).map(item => item.score);
    
    // Define colors
    const primaryColor = '#2E7D32';
    const secondaryColor = '#8BC34A';
    const accentColor = '#FFA000';
    const otherColors = ['#4CAF50', '#81C784'];
    
    // Create a horizontal bar chart
    if (window.confidenceChart) {
        window.confidenceChart.destroy();
    }
    
    window.confidenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top5Crops,
            datasets: [{
                label: 'Confidence Score (%)',
                data: top5Scores,
                backgroundColor: [primaryColor, secondaryColor, accentColor, ...otherColors],
                borderColor: [primaryColor, secondaryColor, accentColor, ...otherColors],
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Confidence: ${context.raw.toFixed(2)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Confidence (%)'
                    }
                }
            }
        }
    });
}

// Create a chart showing the comparison between user input and optimal parameters
function createParameterComparisonChart(data, conditions) {
    const ctx = document.getElementById('parameter-chart').getContext('2d');
    const formData = new FormData(document.getElementById('recommendation-form'));
    
    // Get user input values
    const userValues = {
        n: parseFloat(formData.get('nitrogen')),
        p: parseFloat(formData.get('phosphorus')),
        k: parseFloat(formData.get('potassium')),
        temp: parseFloat(formData.get('temperature')),
        humidity: parseFloat(formData.get('humidity')),
        ph: parseFloat(formData.get('ph')),
        rainfall: parseFloat(formData.get('rainfall'))
    };
    
    // Calculate normalized values for better visualization
    // For each parameter, we'll normalize values between 0 and 100
    const normalize = (value, min, max) => {
        return ((value - min) / (max - min)) * 100;
    };
    
    // Define parameter ranges (min/max possible values)
    const ranges = {
        n: [0, 140],
        p: [5, 145],
        k: [5, 205],
        temp: [0, 50],
        humidity: [0, 100],
        ph: [0, 14],
        rainfall: [0, 300]
    };
    
    // Normalize user values
    const normalizedUserValues = {
        n: normalize(userValues.n, ranges.n[0], ranges.n[1]),
        p: normalize(userValues.p, ranges.p[0], ranges.p[1]),
        k: normalize(userValues.k, ranges.k[0], ranges.k[1]),
        temp: normalize(userValues.temp, ranges.temp[0], ranges.temp[1]),
        humidity: normalize(userValues.humidity, ranges.humidity[0], ranges.humidity[1]),
        ph: normalize(userValues.ph, ranges.ph[0], ranges.ph[1]),
        rainfall: normalize(userValues.rainfall, ranges.rainfall[0], ranges.rainfall[1])
    };
    
    // Normalize optimal min values
    const normalizedOptimalMin = {
        n: normalize(conditions.n_min, ranges.n[0], ranges.n[1]),
        p: normalize(conditions.p_min, ranges.p[0], ranges.p[1]),
        k: normalize(conditions.k_min, ranges.k[0], ranges.k[1]),
        temp: normalize(conditions.temperature_min, ranges.temp[0], ranges.temp[1]),
        humidity: normalize(conditions.humidity_min, ranges.humidity[0], ranges.humidity[1]),
        ph: normalize(conditions.ph_min, ranges.ph[0], ranges.ph[1]),
        rainfall: normalize(conditions.rainfall_min, ranges.rainfall[0], ranges.rainfall[1])
    };
    
    // Normalize optimal max values
    const normalizedOptimalMax = {
        n: normalize(conditions.n_max, ranges.n[0], ranges.n[1]),
        p: normalize(conditions.p_max, ranges.p[0], ranges.p[1]),
        k: normalize(conditions.k_max, ranges.k[0], ranges.k[1]),
        temp: normalize(conditions.temperature_max, ranges.temp[0], ranges.temp[1]),
        humidity: normalize(conditions.humidity_max, ranges.humidity[0], ranges.humidity[1]),
        ph: normalize(conditions.ph_max, ranges.ph[0], ranges.ph[1]),
        rainfall: normalize(conditions.rainfall_max, ranges.rainfall[0], ranges.rainfall[1])
    };
    
    // Calculate optimal range width
    const optimalRangeWidth = {
        n: normalizedOptimalMax.n - normalizedOptimalMin.n,
        p: normalizedOptimalMax.p - normalizedOptimalMin.p,
        k: normalizedOptimalMax.k - normalizedOptimalMin.k,
        temp: normalizedOptimalMax.temp - normalizedOptimalMin.temp,
        humidity: normalizedOptimalMax.humidity - normalizedOptimalMin.humidity,
        ph: normalizedOptimalMax.ph - normalizedOptimalMin.ph,
        rainfall: normalizedOptimalMax.rainfall - normalizedOptimalMin.rainfall
    };
    
    // Define colors
    const primaryColor = '#2E7D32';
    const secondaryColor = 'rgba(139, 195, 74, 0.3)';
    const secondaryBorderColor = '#8BC34A';
    
    if (window.parameterChart) {
        window.parameterChart.destroy();
    }
    
    window.parameterChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
            datasets: [
                {
                    label: 'Your Soil',
                    data: [
                        normalizedUserValues.n,
                        normalizedUserValues.p,
                        normalizedUserValues.k,
                        normalizedUserValues.temp,
                        normalizedUserValues.humidity,
                        normalizedUserValues.ph,
                        normalizedUserValues.rainfall
                    ],
                    backgroundColor: primaryColor,
                    barPercentage: 0.4
                },
                {
                    label: 'Optimal Range',
                    data: [
                        optimalRangeWidth.n,
                        optimalRangeWidth.p,
                        optimalRangeWidth.k,
                        optimalRangeWidth.temp,
                        optimalRangeWidth.humidity,
                        optimalRangeWidth.ph,
                        optimalRangeWidth.rainfall
                    ],
                    backgroundColor: secondaryColor,
                    borderColor: secondaryBorderColor,
                    borderWidth: 1,
                    barPercentage: 0.8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: false
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Normalized Value (%)'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            return tooltipItems[0].label;
                        },
                        label: function(context) {
                            const paramMap = {
                                'Nitrogen': 'n',
                                'Phosphorus': 'p',
                                'Potassium': 'k',
                                'Temperature': 'temp',
                                'Humidity': 'humidity',
                                'pH': 'ph',
                                'Rainfall': 'rainfall'
                            };
                            
                            const unitMap = {
                                'n': 'kg/ha',
                                'p': 'kg/ha',
                                'k': 'kg/ha',
                                'temp': '°C',
                                'humidity': '%',
                                'ph': '',
                                'rainfall': 'mm'
                            };
                            
                            const param = paramMap[context.label];
                            const unit = unitMap[param];
                            
                            if (context.datasetIndex === 0) {
                                return `Your value: ${userValues[param]} ${unit}`;
                            } else {
                                const paramNameMap = {
                                    'n': 'n',
                                    'p': 'p',
                                    'k': 'k',
                                    'temp': 'temperature',
                                    'humidity': 'humidity',
                                    'ph': 'ph',
                                    'rainfall': 'rainfall'
                                };
                                
                                const conditionMin = conditions[`${paramNameMap[param]}_min`];
                                const conditionMax = conditions[`${paramNameMap[param]}_max`];
                                
                                return `Optimal range: ${conditionMin} - ${conditionMax} ${unit}`;
                            }
                        }
                    }
                }
            }
        }
    });
}

// Create a range chart for the reverse lookup feature
function createRangeChart(cropName, conditions) {
    const ctx = document.getElementById('range-chart').getContext('2d');
    
    // Define parameters and their ranges
    const parameters = [
        { name: 'Nitrogen', min: conditions.n_min, max: conditions.n_max, unit: 'kg/ha', totalRange: [0, 140] },
        { name: 'Phosphorus', min: conditions.p_min, max: conditions.p_max, unit: 'kg/ha', totalRange: [5, 145] },
        { name: 'Potassium', min: conditions.k_min, max: conditions.k_max, unit: 'kg/ha', totalRange: [5, 205] },
        { name: 'Temperature', min: conditions.temperature_min, max: conditions.temperature_max, unit: '°C', totalRange: [0, 50] },
        { name: 'Humidity', min: conditions.humidity_min, max: conditions.humidity_max, unit: '%', totalRange: [0, 100] },
        { name: 'pH', min: conditions.ph_min, max: conditions.ph_max, unit: '', totalRange: [0, 14] },
        { name: 'Rainfall', min: conditions.rainfall_min, max: conditions.rainfall_max, unit: 'mm', totalRange: [0, 300] }
    ];
    
    // Calculate percentages for positioning
    const data = parameters.map(param => {
        const totalRange = param.totalRange[1] - param.totalRange[0];
        const minPercent = ((param.min - param.totalRange[0]) / totalRange) * 100;
        const maxPercent = ((param.max - param.totalRange[0]) / totalRange) * 100;
        const rangeWidth = maxPercent - minPercent;
        
        return {
            parameter: param.name,
            unit: param.unit,
            minValue: param.min,
            maxValue: param.max,
            startPosition: minPercent,
            rangeWidth: rangeWidth
        };
    });
    
    if (window.rangeChart) {
        window.rangeChart.destroy();
    }
    
    window.rangeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.parameter),
            datasets: [
                {
                    label: 'Parameter Range',
                    data: data.map(d => d.rangeWidth),
                    backgroundColor: '#8BC34A',
                    barPercentage: 0.8,
                    base: data.map(d => d.startPosition)
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Range (% of possible values)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(tooltipItems) {
                            return tooltipItems[0].label;
                        },
                        label: function(context) {
                            const index = context.dataIndex;
                            return `Optimal range: ${data[index].minValue} - ${data[index].maxValue} ${data[index].unit}`;
                        }
                    }
                }
            }
        }
    });
}

// Helper function to capitalize the first letter of each word
function capitalizeFirstLetter(string) {
    return string.split(' ').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}
