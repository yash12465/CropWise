import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from crop_recommender import CropRecommender

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize crop recommender
crop_recommender = CropRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/crop_encyclopedia')
def crop_encyclopedia():
    return render_template('crop_encyclopedia.html')

@app.route('/reverse_lookup')
def reverse_lookup():
    return render_template('reverse_lookup.html')

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server error: {str(e)}")
    return render_template('index.html'), 500
