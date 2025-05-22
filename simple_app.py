import os
import logging
import csv
import json
from io import StringIO
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from simple_crop_recommender import SimpleCropRecommender
from weather_service import weather_service
from pest_disease_detector import pest_disease_detector

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Initialize services
crop_recommender = SimpleCropRecommender()

# Create initial market price data if it doesn't exist
def initialize_market_prices():
    try:
        if not os.path.exists('market_prices.json'):
            # Create sample market price data
            market_data = {
                "last_updated": datetime.now().isoformat(),
                "prices": {
                    "rice": {
                        "current_price": 24.50,
                        "last_month_price": 22.75,
                        "unit": "per 50kg",
                        "trend": "up",
                        "percent_change": 7.69
                    },
                    "wheat": {
                        "current_price": 18.20,
                        "last_month_price": 19.40,
                        "unit": "per 50kg",
                        "trend": "down",
                        "percent_change": -6.19
                    },
                    "maize": {
                        "current_price": 14.75,
                        "last_month_price": 13.90,
                        "unit": "per 50kg",
                        "trend": "up",
                        "percent_change": 6.12
                    },
                    "beans": {
                        "current_price": 89.00,
                        "last_month_price": 85.50,
                        "unit": "per 50kg",
                        "trend": "up",
                        "percent_change": 4.09
                    },
                    "potatoes": {
                        "current_price": 32.50,
                        "last_month_price": 35.75,
                        "unit": "per 50kg",
                        "trend": "down",
                        "percent_change": -9.09
                    },
                    "tomatoes": {
                        "current_price": 45.00,
                        "last_month_price": 38.25,
                        "unit": "per 20kg box",
                        "trend": "up",
                        "percent_change": 17.65
                    },
                    "onions": {
                        "current_price": 28.75,
                        "last_month_price": 30.00,
                        "unit": "per 25kg",
                        "trend": "down",
                        "percent_change": -4.17
                    },
                    "cabbage": {
                        "current_price": 15.90,
                        "last_month_price": 14.75,
                        "unit": "per 30kg",
                        "trend": "up",
                        "percent_change": 7.80
                    }
                },
                "markets": [
                    {"name": "Central Farmers Market", "location": "New Delhi", "country": "India"},
                    {"name": "Global Agri-Trade Center", "location": "Chicago", "country": "USA"},
                    {"name": "European Crop Exchange", "location": "Paris", "country": "France"},
                    {"name": "Agricultural Products Market", "location": "Beijing", "country": "China"},
                    {"name": "Southern Hemisphere Exchange", "location": "São Paulo", "country": "Brazil"}
                ]
            }
            
            # Save market data to file
            with open('market_prices.json', 'w') as f:
                json.dump(market_data, f, indent=2)
                
            logging.info("Created initial market price data")
    except Exception as e:
        logging.error(f"Error initializing market prices: {str(e)}")

# Initialize market prices
initialize_market_prices()

# Function to load market prices
def load_market_prices():
    try:
        with open('market_prices.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading market prices: {str(e)}")
        return {"prices": {}, "last_updated": datetime.now().isoformat()}

# Create farming calendar data if it doesn't exist
def initialize_farming_calendar():
    try:
        if not os.path.exists('farming_calendar.json'):
            # Create sample farming calendar data
            calendar_data = {
                "rice": {
                    "planting_season": {
                        "start": {"month": 5, "day": 1},  # May 1
                        "end": {"month": 6, "day": 15}    # June 15
                    },
                    "growing_season": {
                        "start": {"month": 6, "day": 15}, # June 15
                        "end": {"month": 9, "day": 15}    # September 15
                    },
                    "harvest_season": {
                        "start": {"month": 9, "day": 15}, # September 15
                        "end": {"month": 10, "day": 31}   # October 31
                    },
                    "key_activities": [
                        {"month": 4, "activity": "Prepare soil and seedbeds"},
                        {"month": 5, "activity": "Sow seeds or transplant seedlings"},
                        {"month": 6, "activity": "Apply fertilizer and manage water levels"},
                        {"month": 7, "activity": "Monitor for pests and diseases"},
                        {"month": 8, "activity": "Maintain water levels and prepare for harvest"},
                        {"month": 9, "activity": "Drain fields before harvest"},
                        {"month": 10, "activity": "Harvest and dry rice grains"}
                    ]
                },
                "maize": {
                    "planting_season": {
                        "start": {"month": 3, "day": 15}, # March 15
                        "end": {"month": 5, "day": 15}    # May 15
                    },
                    "growing_season": {
                        "start": {"month": 5, "day": 15}, # May 15
                        "end": {"month": 7, "day": 31}    # July 31
                    },
                    "harvest_season": {
                        "start": {"month": 8, "day": 1},  # August 1
                        "end": {"month": 9, "day": 30}    # September 30
                    },
                    "key_activities": [
                        {"month": 2, "activity": "Prepare soil with fertilizer"},
                        {"month": 3, "activity": "Plant seeds when soil temperature is warm enough"},
                        {"month": 4, "activity": "Monitor for weeds and pests"},
                        {"month": 5, "activity": "Apply side-dressing of nitrogen"},
                        {"month": 6, "activity": "Monitor for corn borers and other pests"},
                        {"month": 7, "activity": "Ensure adequate irrigation during tasseling"},
                        {"month": 8, "activity": "Prepare for harvest when kernels are dented"}
                    ]
                },
                "wheat": {
                    "planting_season": {
                        "start": {"month": 9, "day": 15}, # September 15 (winter wheat)
                        "end": {"month": 11, "day": 15}   # November 15
                    },
                    "growing_season": {
                        "start": {"month": 11, "day": 15}, # November 15
                        "end": {"month": 5, "day": 15}    # May 15
                    },
                    "harvest_season": {
                        "start": {"month": 5, "day": 15}, # May 15
                        "end": {"month": 7, "day": 15}    # July 15
                    },
                    "key_activities": [
                        {"month": 8, "activity": "Prepare soil for planting"},
                        {"month": 9, "activity": "Plant winter wheat"},
                        {"month": 10, "activity": "Apply pre-emergent herbicides"},
                        {"month": 3, "activity": "Apply nitrogen fertilizer as growth resumes"},
                        {"month": 4, "activity": "Monitor for rust and other diseases"},
                        {"month": 5, "activity": "Prepare harvest equipment"},
                        {"month": 6, "activity": "Harvest when grain moisture is proper"}
                    ]
                }
            }
            
            # Add more crops based on our recommender data
            for crop in crop_recommender.get_all_crops():
                if crop not in calendar_data and crop != "label":
                    # Add basic calendar data for each crop in our recommender
                    calendar_data[crop] = {
                        "planting_season": {
                            "start": {"month": 3, "day": 1},  # Default to Spring planting
                            "end": {"month": 5, "day": 30}
                        },
                        "growing_season": {
                            "start": {"month": 5, "day": 30},
                            "end": {"month": 8, "day": 30}
                        },
                        "harvest_season": {
                            "start": {"month": 8, "day": 30},
                            "end": {"month": 10, "day": 30}
                        },
                        "key_activities": [
                            {"month": 2, "activity": "Prepare soil for planting"},
                            {"month": 3, "activity": "Begin planting in warm areas"},
                            {"month": 4, "activity": "Continue planting as soil warms"},
                            {"month": 5, "activity": "Monitor for pests and diseases"},
                            {"month": 8, "activity": "Prepare for harvest"},
                            {"month": 9, "activity": "Harvest when mature"}
                        ]
                    }
            
            # Save calendar data to file
            with open('farming_calendar.json', 'w') as f:
                json.dump(calendar_data, f, indent=2)
                
            logging.info("Created initial farming calendar data")
    except Exception as e:
        logging.error(f"Error initializing farming calendar: {str(e)}")

# Initialize farming calendar
initialize_farming_calendar()

# Function to load farming calendar
def load_farming_calendar():
    try:
        with open('farming_calendar.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading farming calendar: {str(e)}")
        return {}

@app.route('/')
def index():
    return render_template('simple_index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/crop_encyclopedia')
def crop_encyclopedia():
    return render_template('crop_encyclopedia.html')

@app.route('/reverse_lookup')
def reverse_lookup():
    return render_template('reverse_lookup.html')

@app.route('/soil_health')
def soil_health():
    return render_template('soil_health.html')

@app.route('/yield_predictor')
def yield_predictor():
    return render_template('yield_predictor.html')

@app.route('/data_upload')
def data_upload():
    return render_template('data_upload.html')

@app.route('/weather_dashboard')
def weather_dashboard():
    # Store the user's location in session if provided
    location = request.args.get('location')
    if location and isinstance(location, str) and location.strip():
        session['weather_location'] = location
    
    # Use stored location or default
    current_location = session.get('weather_location', 'New York')
    
    return render_template('weather_dashboard.html', location=current_location)

@app.route('/market_prices')
def market_prices():
    # Load market price data
    market_data = load_market_prices()
    return render_template('market_prices.html', market_data=market_data)

@app.route('/pest_disease_identification')
def pest_disease_identification():
    # Get all crops for the dropdown
    crops = pest_disease_detector.get_all_crops()
    return render_template('pest_disease.html', crops=crops)

@app.route('/farming_calendar')
def farming_calendar():
    # Get selected crop or default to first crop
    selected_crop = request.args.get('crop', '')
    
    # Load calendar data
    calendar_data = load_farming_calendar()
    
    # Get all available crops
    available_crops = list(calendar_data.keys())
    
    # If no crop selected or invalid crop, default to first available
    if not selected_crop or selected_crop not in available_crops:
        if available_crops:
            selected_crop = available_crops[0]
        else:
            selected_crop = None
    
    return render_template('farming_calendar.html', 
                          calendar_data=calendar_data,
                          available_crops=available_crops,
                          selected_crop=selected_crop)

@app.route('/irrigation_planner')
def irrigation_planner():
    return render_template('irrigation_planner.html')

@app.route('/carbon_footprint_calculator')
def carbon_footprint_calculator():
    return render_template('carbon_footprint.html')

@app.route('/farm_equipment_guide')
def farm_equipment_guide():
    return render_template('equipment_guide.html')

@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    try:
        # Get soil parameters from form
        n_value = request.form.get('nitrogen')
        p_value = request.form.get('phosphorus')
        k_value = request.form.get('potassium')
        temp_value = request.form.get('temperature')
        humidity_value = request.form.get('humidity')
        ph_value = request.form.get('ph')
        rainfall_value = request.form.get('rainfall')
        
        # Validate and convert parameters
        if not all([n_value, p_value, k_value, temp_value, humidity_value, ph_value, rainfall_value]):
            return jsonify({
                'success': False,
                'error': 'All soil parameters are required'
            }), 400
            
        try:
            n = float(n_value)
            p = float(p_value)
            k = float(k_value)
            temperature = float(temp_value)
            humidity = float(humidity_value)
            ph = float(ph_value)
            rainfall = float(rainfall_value)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'All parameters must be valid numbers'
            }), 400
        
        # Get recommendation
        recommended_crop, confidence_scores = crop_recommender.predict(
            n, p, k, temperature, humidity, ph, rainfall
        )
        
        # Get weather data if API key is available
        weather_data = None
        location = request.form.get('location')
        if location and os.environ.get("OPENWEATHERMAP_API_KEY"):
            try:
                weather_data = weather_service.get_current_weather(location)
            except Exception as we:
                logging.error(f"Error fetching weather data: {str(we)}")
        
        # Return recommendation
        response_data = {
            'success': True,
            'crop': recommended_crop,
            'confidence_scores': confidence_scores
        }
        
        # Add weather data if available
        if weather_data and weather_data.get('success'):
            response_data['weather'] = weather_data
        
        return jsonify(response_data)
    except Exception as e:
        logging.error(f"Error in recommendation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/crop_conditions', methods=['GET'])
def get_crop_conditions():
    crop_name = request.args.get('crop')
    if not crop_name:
        return jsonify({
            'success': False,
            'error': 'Crop name is required'
        }), 400
    
    try:
        conditions = crop_recommender.get_optimal_conditions(crop_name)
        return jsonify({
            'success': True,
            'conditions': conditions
        })
    except Exception as e:
        logging.error(f"Error getting crop conditions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/crops', methods=['GET'])
def get_crops():
    return jsonify({
        'success': True,
        'crops': crop_recommender.get_all_crops()
    })

@app.route('/api/analyze_soil', methods=['POST'])
def analyze_soil():
    try:
        # Get soil parameters from form
        n = float(request.form.get('nitrogen'))
        p = float(request.form.get('phosphorus'))
        k = float(request.form.get('potassium'))
        ph = float(request.form.get('ph'))
        
        # Analyze soil health
        health_report = crop_recommender.analyze_soil_health(n, p, k, ph)
        
        # Return soil health report
        return jsonify({
            'success': True,
            'health_report': health_report
        })
    except Exception as e:
        logging.error(f"Error analyzing soil health: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/predict_yield', methods=['POST'])
def predict_yield():
    try:
        # Get parameters from form
        crop = request.form.get('crop')
        n = float(request.form.get('nitrogen'))
        p = float(request.form.get('phosphorus'))
        k = float(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
        
        # Predict yield
        yield_prediction = crop_recommender.predict_yield(
            crop, n, p, k, temperature, humidity, ph, rainfall
        )
        
        # Return yield prediction
        return jsonify(yield_prediction)
    except Exception as e:
        logging.error(f"Error predicting yield: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/suitable_crops', methods=['POST'])
def find_suitable_crops():
    try:
        # Get soil parameters from form
        n = float(request.form.get('nitrogen'))
        p = float(request.form.get('phosphorus'))
        k = float(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
        
        # Find suitable crops
        suitable_crops = crop_recommender.find_suitable_crops(
            n, p, k, temperature, humidity, ph, rainfall
        )
        
        # Return suitable crops
        return jsonify({
            'success': True,
            'suitable_crops': suitable_crops[:10]  # Return top 10 crops
        })
    except Exception as e:
        logging.error(f"Error finding suitable crops: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    try:
        if 'csv_file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['csv_file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Read CSV file
        content = file.read().decode('utf-8')
        csv_file = StringIO(content)
        
        # Validate CSV structure
        try:
            reader = csv.reader(csv_file)
            header = next(reader)
            
            # Check required columns
            required_columns = ['label', 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            missing_columns = [col for col in required_columns if col not in header]
            
            if missing_columns:
                return jsonify({
                    'success': False,
                    'error': f'Missing required columns: {", ".join(missing_columns)}'
                }), 400
                
            # Reset file pointer
            csv_file.seek(0)
            
            # Save the file temporarily
            temp_file_path = f'uploaded_data_{os.urandom(4).hex()}.csv'
            with open(temp_file_path, 'w') as f:
                f.write(content)
            
            # Load crop data from the CSV
            crop_recommender.load_crop_data_from_csv(temp_file_path)
            
            # Clean up the temporary file
            os.remove(temp_file_path)
            
            return jsonify({
                'success': True,
                'message': f'Successfully loaded crop data from CSV file',
                'crop_count': len(crop_recommender.get_all_crops())
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Invalid CSV format: {str(e)}'
            }), 400
    except Exception as e:
        logging.error(f"Error uploading CSV: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('simple_index.html'), 404

@app.route('/api/weather/current', methods=['GET'])
def get_weather():
    try:
        location = request.args.get('location')
        if not location or not isinstance(location, str) or not location.strip():
            return jsonify({
                'success': False,
                'error': 'Location is required'
            }), 400
            
        weather_data = weather_service.get_current_weather(location)
        return jsonify(weather_data)
    except Exception as e:
        logging.error(f"Error getting weather data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather/forecast', methods=['GET'])
def get_weather_forecast():
    try:
        location = request.args.get('location')
        days_str = request.args.get('days', '5')
        
        if not location or not isinstance(location, str) or not location.strip():
            return jsonify({
                'success': False,
                'error': 'Location is required'
            }), 400
            
        try:
            days = int(days_str)
            if days < 1 or days > 7:
                days = 5  # Default to 5 days if out of range
        except ValueError:
            days = 5  # Default to 5 days if invalid
            
        forecast_data = weather_service.get_forecast(location, days)
        return jsonify(forecast_data)
    except Exception as e:
        logging.error(f"Error getting weather forecast: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/market_prices', methods=['GET'])
def get_market_prices():
    try:
        crop = request.args.get('crop')
        market_data = load_market_prices()
        
        if crop and isinstance(crop, str) and crop.strip():
            crop = crop.lower().strip()
            if crop in market_data.get('prices', {}):
                return jsonify({
                    'success': True,
                    'crop': crop,
                    'price_data': market_data['prices'][crop],
                    'last_updated': market_data.get('last_updated')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'No price data available for {crop}'
                }), 404
        else:
            # Return all prices
            return jsonify({
                'success': True,
                'market_data': market_data
            })
    except Exception as e:
        logging.error(f"Error getting market prices: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/pests_diseases', methods=['GET'])
def get_pests_diseases():
    try:
        crop = request.args.get('crop')
        if not crop or not isinstance(crop, str) or not crop.strip():
            return jsonify({
                'success': False,
                'error': 'Crop name is required'
            }), 400
            
        pest_disease_data = pest_disease_detector.get_common_pests_diseases(crop)
        return jsonify(pest_disease_data)
    except Exception as e:
        logging.error(f"Error getting pest and disease data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/identify_pest_disease', methods=['POST'])
def identify_pest_disease():
    try:
        crop = request.form.get('crop')
        symptoms_str = request.form.get('symptoms')
        
        if not crop or not isinstance(crop, str) or not crop.strip():
            return jsonify({
                'success': False,
                'error': 'Crop name is required'
            }), 400
            
        if not symptoms_str or not isinstance(symptoms_str, str) or not symptoms_str.strip():
            return jsonify({
                'success': False,
                'error': 'Symptoms are required'
            }), 400
            
        # Parse symptoms from comma-separated string
        symptoms = [s.strip() for s in symptoms_str.split(',') if s.strip()]
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'At least one symptom is required'
            }), 400
            
        identification_results = pest_disease_detector.identify_issue(crop, symptoms)
        return jsonify(identification_results)
    except Exception as e:
        logging.error(f"Error identifying pest or disease: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/farming_calendar', methods=['GET'])
def get_farming_calendar():
    try:
        crop = request.args.get('crop')
        calendar_data = load_farming_calendar()
        
        if crop and isinstance(crop, str) and crop.strip():
            crop = crop.lower().strip()
            if crop in calendar_data:
                return jsonify({
                    'success': True,
                    'crop': crop,
                    'calendar_data': calendar_data[crop]
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'No calendar data available for {crop}'
                }), 404
        else:
            # Return all calendar data
            return jsonify({
                'success': True,
                'available_crops': list(calendar_data.keys()),
                'calendar_data': calendar_data
            })
    except Exception as e:
        logging.error(f"Error getting farming calendar: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/carbon_footprint', methods=['POST'])
def calculate_carbon_footprint():
    try:
        # Get form data with proper validation
        farm_size_str = request.form.get('farm_size', '0')
        crop_type = request.form.get('crop_type', '')
        fertilizer_amount_str = request.form.get('fertilizer_amount', '0')
        machinery_hours_str = request.form.get('machinery_hours', '0')
        irrigation_water_str = request.form.get('irrigation_water', '0')
        
        # Validate and convert to appropriate types
        try:
            farm_size = float(farm_size_str) if farm_size_str else 0
            fertilizer_amount = float(fertilizer_amount_str) if fertilizer_amount_str else 0
            machinery_hours = float(machinery_hours_str) if machinery_hours_str else 0
            irrigation_water = float(irrigation_water_str) if irrigation_water_str else 0
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'All numeric values must be valid numbers'
            }), 400
            
        # Simplified carbon footprint calculation
        # These are simplified emission factors
        emissions = {
            'land_use': farm_size * 0.5,  # 0.5 tonnes CO2e per hectare
            'fertilizer': fertilizer_amount * 0.004,  # 4 kg CO2e per kg fertilizer
            'machinery': machinery_hours * 10,  # 10 kg CO2e per hour of machinery use
            'irrigation': irrigation_water * 0.0005,  # 0.5 kg CO2e per cubic meter of water
        }
        
        # Crop-specific factor
        crop_factors = {
            'rice': 1.5,
            'wheat': 0.8,
            'maize': 0.7,
            'beans': 0.3,
            'potatoes': 0.4,
            'cotton': 1.2,
            'coffee': 1.0
        }
        
        crop_factor = crop_factors.get(crop_type.lower(), 1.0)
        
        # Calculate total emissions in tonnes CO2e
        total_emissions = sum(emissions.values()) * crop_factor
        
        # Carbon sequestration potential (simplified)
        sequestration_potential = farm_size * 0.3  # 0.3 tonnes CO2e per hectare
        
        # Net carbon footprint
        net_footprint = total_emissions - sequestration_potential
        
        # Recommendations to reduce footprint
        recommendations = []
        if emissions['fertilizer'] > 2:
            recommendations.append("Consider reducing fertilizer use or switching to organic alternatives.")
        if emissions['machinery'] > 10:
            recommendations.append("Optimize machinery operations or consider more fuel-efficient equipment.")
        if emissions['irrigation'] > 5:
            recommendations.append("Implement more efficient irrigation systems like drip irrigation.")
        
        return jsonify({
            'success': True,
            'emissions': {
                'land_use': round(emissions['land_use'], 2),
                'fertilizer': round(emissions['fertilizer'], 2),
                'machinery': round(emissions['machinery'], 2),
                'irrigation': round(emissions['irrigation'], 2),
                'total': round(total_emissions, 2),
            },
            'sequestration_potential': round(sequestration_potential, 2),
            'net_footprint': round(net_footprint, 2),
            'recommendations': recommendations
        })
    except Exception as e:
        logging.error(f"Error calculating carbon footprint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {str(e)}")
    return render_template('simple_index.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
