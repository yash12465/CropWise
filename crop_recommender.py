import os
import json
import pickle
import logging
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from models import CropConditions

class CropRecommender:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.crop_data = None
        self.initialize_model()
        self.load_crop_data()
    
    def initialize_model(self):
        """
        Initialize the crop recommendation model. If pre-trained model exists, load it.
        Otherwise, train a new model.
        """
        try:
            # Try to load pre-trained model
            with open('crop_recommender.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            logging.info("Loaded pre-trained model and scaler")
        except FileNotFoundError:
            logging.info("No pre-trained model found. Training new model...")
            self.train_model()
    
    def load_crop_data(self):
        """Load crop data with optimal growing conditions"""
        try:
            with open('static/assets/crop_data.json', 'r') as f:
                self.crop_data = json.load(f)
        except FileNotFoundError:
            # Create default crop data if file doesn't exist
            self.crop_data = self._create_default_crop_data()
            # Save the data
            os.makedirs('static/assets', exist_ok=True)
            with open('static/assets/crop_data.json', 'w') as f:
                json.dump(self.crop_data, f, indent=4)
    
    def _create_default_crop_data(self):
        """Create default crop data with optimal growing conditions"""
        # Sample data - in a real app, this would come from a comprehensive database
        return {
            "rice": {
                "n_min": 60, "n_max": 100,
                "p_min": 35, "p_max": 60,
                "k_min": 35, "k_max": 45,
                "temperature_min": 20, "temperature_max": 27,
                "humidity_min": 80, "humidity_max": 85,
                "ph_min": 5.0, "ph_max": 8.0,
                "rainfall_min": 180, "rainfall_max": 300,
                "description": "Rice is a staple food for over half the world's population. It grows best in warm, humid environments with plenty of water."
            },
            "maize": {
                "n_min": 60, "n_max": 100,
                "p_min": 35, "p_max": 60,
                "k_min": 15, "k_max": 25,
                "temperature_min": 18, "temperature_max": 26,
                "humidity_min": 55, "humidity_max": 75,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 60, "rainfall_max": 110,
                "description": "Maize (corn) is one of the most versatile crops, used for food, feed, and industrial products. It prefers warm soil and good drainage."
            },
            "chickpea": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 15, "temperature_max": 25,
                "humidity_min": 20, "humidity_max": 40,
                "ph_min": 6.0, "ph_max": 8.0,
                "rainfall_min": 40, "rainfall_max": 100,
                "description": "Chickpeas are drought-resistant legumes rich in protein. They grow well in semi-arid regions with moderate temperatures."
            },
            "kidneybeans": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 18, "temperature_max": 30,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.5,
                "rainfall_min": 60, "rainfall_max": 150,
                "description": "Kidney beans require warm temperatures and moderate rainfall. They are nitrogen-fixing plants that improve soil fertility."
            },
            "pigeonpeas": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 20, "temperature_max": 35,
                "humidity_min": 50, "humidity_max": 80,
                "ph_min": 5.0, "ph_max": 7.0,
                "rainfall_min": 60, "rainfall_max": 150,
                "description": "Pigeon peas are drought-resistant legumes that can grow in marginal soils. They are an important source of protein in many regions."
            },
            "mothbeans": {
                "n_min": 15, "n_max": 45,
                "p_min": 35, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 25, "temperature_max": 35,
                "humidity_min": 30, "humidity_max": 60,
                "ph_min": 6.0, "ph_max": 7.5,
                "rainfall_min": 40, "rainfall_max": 100,
                "description": "Moth beans are heat and drought tolerant, making them suitable for arid and semi-arid regions with limited rainfall."
            },
            "mungbean": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 20, "temperature_max": 35,
                "humidity_min": 50, "humidity_max": 80,
                "ph_min": 6.0, "ph_max": 7.5,
                "rainfall_min": 60, "rainfall_max": 150,
                "description": "Mung beans are fast-growing legumes that prefer warm temperatures and moderate humidity. They are commonly used for sprouts."
            },
            "blackgram": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 20, "temperature_max": 35,
                "humidity_min": 50, "humidity_max": 80,
                "ph_min": 6.0, "ph_max": 7.5,
                "rainfall_min": 60, "rainfall_max": 150,
                "description": "Black gram is a drought-resistant legume that grows well in a variety of soil types. It's an important source of protein."
            },
            "lentil": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 15, "temperature_max": 25,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 6.0, "ph_max": 8.0,
                "rainfall_min": 40, "rainfall_max": 100,
                "description": "Lentils are cool-season legumes that are relatively drought tolerant. They are a good source of protein and fiber."
            },
            "pomegranate": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 18, "temperature_max": 35,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.5,
                "rainfall_min": 50, "rainfall_max": 100,
                "description": "Pomegranates are drought-tolerant fruit trees that prefer hot, dry summers and cool winters. They can grow in a variety of soil types."
            },
            "banana": {
                "n_min": 75, "n_max": 100,
                "p_min": 45, "p_max": 75,
                "k_min": 25, "k_max": 55,
                "temperature_min": 20, "temperature_max": 30,
                "humidity_min": 70, "humidity_max": 90,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 120, "rainfall_max": 220,
                "description": "Bananas require consistent moisture and warm temperatures. They are sensitive to frost and wind damage."
            },
            "mango": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 24, "temperature_max": 35,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.5,
                "rainfall_min": 80, "rainfall_max": 180,
                "description": "Mangoes thrive in tropical climates with distinct wet and dry seasons. They are sensitive to frost and cold temperatures."
            },
            "grapes": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 15, "temperature_max": 30,
                "humidity_min": 50, "humidity_max": 80,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 50, "rainfall_max": 100,
                "description": "Grapes prefer warm, dry climates with long growing seasons. Good drainage is essential for grape cultivation."
            },
            "watermelon": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 22, "temperature_max": 30,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 40, "rainfall_max": 100,
                "description": "Watermelons need warm temperatures, plenty of sunlight, and moderate water. They grow best in well-drained, sandy loam soils."
            },
            "muskmelon": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 22, "temperature_max": 30,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 6.0, "ph_max": 7.0,
                "rainfall_min": 40, "rainfall_max": 100,
                "description": "Muskmelons (cantaloupes) require warm temperatures and consistent moisture during the growing season. They are sensitive to frost."
            },
            "apple": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 10, "temperature_max": 25,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 80, "rainfall_max": 120,
                "description": "Apples require a period of winter dormancy (chill hours) and moderate summers. They grow best in well-drained, loamy soils."
            },
            "orange": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 15, "temperature_max": 30,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 80, "rainfall_max": 180,
                "description": "Oranges prefer subtropical climates with mild winters and warm summers. They require regular moisture for optimal fruit production."
            },
            "papaya": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 22, "temperature_max": 35,
                "humidity_min": 60, "humidity_max": 80,
                "ph_min": 6.0, "ph_max": 7.0,
                "rainfall_min": 100, "rainfall_max": 200,
                "description": "Papayas are fast-growing tropical fruits that require warm temperatures and regular moisture. They are sensitive to frost and waterlogging."
            },
            "coconut": {
                "n_min": 15, "n_max": 45,
                "p_min": 45, "p_max": 75,
                "k_min": 15, "k_max": 45,
                "temperature_min": 20, "temperature_max": 35,
                "humidity_min": 70, "humidity_max": 90,
                "ph_min": 5.5, "ph_max": 7.0,
                "rainfall_min": 150, "rainfall_max": 250,
                "description": "Coconuts thrive in tropical coastal areas with high humidity and regular rainfall. They are salt-tolerant and can grow in sandy soils."
            },
            "cotton": {
                "n_min": 60, "n_max": 100,
                "p_min": 35, "p_max": 65,
                "k_min": 15, "k_max": 45,
                "temperature_min": 20, "temperature_max": 35,
                "humidity_min": 40, "humidity_max": 70,
                "ph_min": 5.5, "ph_max": 8.0,
                "rainfall_min": 60, "rainfall_max": 150,
                "description": "Cotton requires a long, warm growing season with plenty of sunshine. It prefers well-drained soils and moderate rainfall."
            },
            "jute": {
                "n_min": 60, "n_max": 100,
                "p_min": 35, "p_max": 65,
                "k_min": 35, "k_max": 55,
                "temperature_min": 25, "temperature_max": 35,
                "humidity_min": 70, "humidity_max": 90,
                "ph_min": 6.0, "ph_max": 7.5,
                "rainfall_min": 120, "rainfall_max": 200,
                "description": "Jute thrives in hot, humid conditions with abundant rainfall. It is often grown in rotation with rice in tropical regions."
            },
            "coffee": {
                "n_min": 15, "n_max": 45,
                "p_min": 35, "p_max": 65,
                "k_min": 15, "k_max": 45,
                "temperature_min": 15, "temperature_max": 25,
                "humidity_min": 50, "humidity_max": 80,
                "ph_min": 5.0, "ph_max": 6.5,
                "rainfall_min": 120, "rainfall_max": 200,
                "description": "Coffee grows best at higher elevations in tropical climates with well-defined wet and dry seasons. It prefers rich, well-drained soils."
            }
        }
    
    def train_model(self):
        """Train a new crop recommendation model using the included dataset"""
        try:
            # Load dataset
            df = pd.read_csv("attached_assets/crop_recommendation (1).csv")
            
            # Clean data
            df = df.drop_duplicates()
            df_cleaned = self._remove_outliers(df)
            
            # Prepare features and target
            X = df_cleaned.drop(columns=['label'])
            y = df_cleaned['label']
            
            # Scale features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model = SVC(kernel='linear', random_state=42, probability=True)
            self.model.fit(X_train, y_train)
            
            # Save model and scaler
            with open('crop_recommender.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            with open('scaler.pkl', 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logging.info("Model trained and saved successfully")
        except Exception as e:
            logging.error(f"Error training model: {str(e)}")
            raise
    
    def _remove_outliers(self, data):
        """Remove outliers from the dataset"""
        numeric_data = data.select_dtypes(include=['number'])
        Q1 = numeric_data.quantile(0.25)
        Q3 = numeric_data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        filtered_data = data[~((numeric_data < lower_bound) | 
                              (numeric_data > upper_bound)).any(axis=1)]
        return filtered_data
    
    def predict(self, n, p, k, temperature, humidity, ph, rainfall):
        """
        Predict the best crop based on soil parameters
        
        Args:
            n: Nitrogen content in soil (kg/ha)
            p: Phosphorus content in soil (kg/ha)
            k: Potassium content in soil (kg/ha)
            temperature: Temperature (°C)
            humidity: Humidity (%)
            ph: pH value of soil
            rainfall: Rainfall (mm)
            
        Returns:
            Tuple of (recommended crop, confidence scores dictionary)
        """
        if not self.model or not self.scaler:
            raise ValueError("Model not initialized. Please initialize the model first.")
        
        # Prepare input
        input_data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
        input_scaled = self.scaler.transform(input_data)
        
        # Get prediction and probabilities
        predicted_crop = self.model.predict(input_scaled)[0]
        probabilities = self.model.predict_proba(input_scaled)[0]
        
        # Get confidence scores for top 5 crops
        classes = self.model.classes_
        confidence_scores = {}
        for i, crop in enumerate(classes):
            confidence_scores[crop] = float(probabilities[i] * 100)
        
        # Sort by confidence and get top 5
        top_crops = dict(sorted(confidence_scores.items(), 
                               key=lambda item: item[1], 
                               reverse=True)[:5])
        
        return predicted_crop, top_crops
    
    def get_optimal_conditions(self, crop_name):
        """
        Get optimal growing conditions for a specific crop
        
        Args:
            crop_name: Name of the crop
            
        Returns:
            Dictionary with optimal ranges for each parameter
        """
        if not self.crop_data:
            raise ValueError("Crop data not loaded")
        
        crop_name = crop_name.lower()
        if crop_name not in self.crop_data:
            raise ValueError(f"No data available for crop: {crop_name}")
        
        return self.crop_data[crop_name]
    
    def get_all_crops(self):
        """Get list of all available crops"""
        if not self.crop_data:
            raise ValueError("Crop data not loaded")
        
        return list(self.crop_data.keys())
