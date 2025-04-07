import os
import logging
import csv
from io import StringIO
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from simple_crop_recommender import SimpleCropRecommender

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize simple crop recommender
crop_recommender = SimpleCropRecommender()

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

@app.route('/api/recommend', methods=['POST'])
def recommend_crop():
    try:
        # Get soil parameters from form
        n = float(request.form.get('nitrogen'))
        p = float(request.form.get('phosphorus'))
        k = float(request.form.get('potassium'))
        temperature = float(request.form.get('temperature'))
        humidity = float(request.form.get('humidity'))
        ph = float(request.form.get('ph'))
        rainfall = float(request.form.get('rainfall'))
        
        # Get recommendation
        recommended_crop, confidence_scores = crop_recommender.predict(
            n, p, k, temperature, humidity, ph, rainfall
        )
        
        # Return recommendation
        return jsonify({
            'success': True,
            'crop': recommended_crop,
            'confidence_scores': confidence_scores
        })
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

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {str(e)}")
    return render_template('simple_index.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
