import os
import csv
import pickle
import logging
import numpy as np
from collections import defaultdict

class SimpleCropRecommender:
    """A simplified crop recommendation system that works entirely offline"""
    
    def __init__(self):
        self.model = None
        self.crop_data = {}
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        self.initialize()
    
    def initialize(self):
        """Initialize the model by loading from file or training a new one"""
        try:
            # Try to load pre-trained model
            with open('crop_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            logging.info("Loaded pre-trained model")
        except FileNotFoundError:
            logging.info("No pre-trained model found. Training new model...")
            self.train_model_from_csv('attached_assets/crop_recommendation (1).csv')
        
        # Load crop data
        self.load_crop_data()
    
    def load_crop_data(self):
        """Load default crop data from CSV file"""
        # Default crop data (will be extended with uploaded data)
        try:
            # Try to load from the default CSV
            self.load_crop_data_from_csv('attached_assets/crop_recommendation (1).csv')
        except Exception as e:
            logging.error(f"Error loading crop data: {str(e)}")
            # Create empty structure if file doesn't exist
            self.crop_data = {}
    
    def load_crop_data_from_csv(self, csv_path):
        """Load crop data from a CSV file"""
        try:
            crop_stats = defaultdict(lambda: {
                'count': 0,
                'n_sum': 0, 'p_sum': 0, 'k_sum': 0,
                'temp_sum': 0, 'humidity_sum': 0, 'ph_sum': 0, 'rainfall_sum': 0,
                'n_min': float('inf'), 'n_max': float('-inf'),
                'p_min': float('inf'), 'p_max': float('-inf'),
                'k_min': float('inf'), 'k_max': float('-inf'),
                'temp_min': float('inf'), 'temp_max': float('-inf'),
                'humidity_min': float('inf'), 'humidity_max': float('-inf'),
                'ph_min': float('inf'), 'ph_max': float('-inf'),
                'rainfall_min': float('inf'), 'rainfall_max': float('-inf'),
            })
            
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    crop = row.get('label', '')
                    if not crop:
                        continue
                    
                    n = float(row.get('N', 0))
                    p = float(row.get('P', 0))
                    k = float(row.get('K', 0))
                    temp = float(row.get('temperature', 0))
                    humidity = float(row.get('humidity', 0))
                    ph = float(row.get('ph', 0))
                    rainfall = float(row.get('rainfall', 0))
                    
                    # Update stats
                    crop_stats[crop]['count'] += 1
                    crop_stats[crop]['n_sum'] += n
                    crop_stats[crop]['p_sum'] += p
                    crop_stats[crop]['k_sum'] += k
                    crop_stats[crop]['temp_sum'] += temp
                    crop_stats[crop]['humidity_sum'] += humidity
                    crop_stats[crop]['ph_sum'] += ph
                    crop_stats[crop]['rainfall_sum'] += rainfall
                    
                    # Update min/max values
                    crop_stats[crop]['n_min'] = min(crop_stats[crop]['n_min'], n)
                    crop_stats[crop]['n_max'] = max(crop_stats[crop]['n_max'], n)
                    crop_stats[crop]['p_min'] = min(crop_stats[crop]['p_min'], p)
                    crop_stats[crop]['p_max'] = max(crop_stats[crop]['p_max'], p)
                    crop_stats[crop]['k_min'] = min(crop_stats[crop]['k_min'], k)
                    crop_stats[crop]['k_max'] = max(crop_stats[crop]['k_max'], k)
                    crop_stats[crop]['temp_min'] = min(crop_stats[crop]['temp_min'], temp)
                    crop_stats[crop]['temp_max'] = max(crop_stats[crop]['temp_max'], temp)
                    crop_stats[crop]['humidity_min'] = min(crop_stats[crop]['humidity_min'], humidity)
                    crop_stats[crop]['humidity_max'] = max(crop_stats[crop]['humidity_max'], humidity)
                    crop_stats[crop]['ph_min'] = min(crop_stats[crop]['ph_min'], ph)
                    crop_stats[crop]['ph_max'] = max(crop_stats[crop]['ph_max'], ph)
                    crop_stats[crop]['rainfall_min'] = min(crop_stats[crop]['rainfall_min'], rainfall)
                    crop_stats[crop]['rainfall_max'] = max(crop_stats[crop]['rainfall_max'], rainfall)
            
            # Create user-friendly crop data dictionary
            for crop, stats in crop_stats.items():
                if stats['count'] > 0:
                    # Add 10% buffer to min/max values to create more realistic ranges
                    n_range = stats['n_max'] - stats['n_min']
                    p_range = stats['p_max'] - stats['p_min']
                    k_range = stats['k_max'] - stats['k_min']
                    temp_range = stats['temp_max'] - stats['temp_min']
                    humidity_range = stats['humidity_max'] - stats['humidity_min']
                    ph_range = stats['ph_max'] - stats['ph_min']
                    rainfall_range = stats['rainfall_max'] - stats['rainfall_min']
                    
                    # Calculate averages for description
                    n_avg = stats['n_sum'] / stats['count']
                    p_avg = stats['p_sum'] / stats['count']
                    k_avg = stats['k_sum'] / stats['count']
                    temp_avg = stats['temp_sum'] / stats['count']
                    humidity_avg = stats['humidity_sum'] / stats['count']
                    ph_avg = stats['ph_sum'] / stats['count']
                    rainfall_avg = stats['rainfall_sum'] / stats['count']
                    
                    # Generate description based on the data
                    description = f"{crop.capitalize()} typically grows well with nitrogen levels around {n_avg:.1f} kg/ha, "
                    description += f"phosphorus around {p_avg:.1f} kg/ha, and potassium around {k_avg:.1f} kg/ha. "
                    description += f"Optimal temperature is approximately {temp_avg:.1f}°C with humidity of {humidity_avg:.1f}%. "
                    description += f"It prefers soil with pH of {ph_avg:.1f} and rainfall of about {rainfall_avg:.1f} mm."
                    
                    # Store in crop data dictionary
                    self.crop_data[crop] = {
                        'n_min': max(0, stats['n_min'] - 0.1 * n_range),
                        'n_max': stats['n_max'] + 0.1 * n_range,
                        'p_min': max(0, stats['p_min'] - 0.1 * p_range),
                        'p_max': stats['p_max'] + 0.1 * p_range,
                        'k_min': max(0, stats['k_min'] - 0.1 * k_range),
                        'k_max': stats['k_max'] + 0.1 * k_range,
                        'temperature_min': max(0, stats['temp_min'] - 0.1 * temp_range),
                        'temperature_max': stats['temp_max'] + 0.1 * temp_range,
                        'humidity_min': max(0, stats['humidity_min'] - 0.1 * humidity_range),
                        'humidity_max': min(100, stats['humidity_max'] + 0.1 * humidity_range),
                        'ph_min': max(0, stats['ph_min'] - 0.1 * ph_range),
                        'ph_max': min(14, stats['ph_max'] + 0.1 * ph_range),
                        'rainfall_min': max(0, stats['rainfall_min'] - 0.1 * rainfall_range),
                        'rainfall_max': stats['rainfall_max'] + 0.1 * rainfall_range,
                        'description': description
                    }
            
            logging.info(f"Loaded crop data from {csv_path} for {len(self.crop_data)} crops")
        except Exception as e:
            logging.error(f"Error loading crop data from {csv_path}: {str(e)}")
            raise
    
    def train_model_from_csv(self, csv_path):
        """Train a simple custom ML model using our own implementation"""
        try:
            # Read data from CSV
            x_data = []
            y_data = []
            crop_map = {}  # Map crop names to numeric values
            crop_idx = 0
            
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Extract features
                    features = [
                        float(row.get('N', 0)),
                        float(row.get('P', 0)),
                        float(row.get('K', 0)),
                        float(row.get('temperature', 0)),
                        float(row.get('humidity', 0)),
                        float(row.get('ph', 0)),
                        float(row.get('rainfall', 0))
                    ]
                    x_data.append(features)
                    
                    # Extract target (crop name)
                    crop = row.get('label', '')
                    if crop not in crop_map:
                        crop_map[crop] = crop_idx
                        crop_idx += 1
                    
                    y_data.append(crop_map[crop])
            
            # Convert to numpy arrays for faster computation
            x_array = np.array(x_data)
            y_array = np.array(y_data)
            
            # Normalize the data
            x_mean = np.mean(x_array, axis=0)
            x_std = np.std(x_array, axis=0)
            x_norm = (x_array - x_mean) / (x_std + 1e-8)  # Add small epsilon to avoid division by zero
            
            # Train a simple k-nearest neighbors model
            self.model = {
                'x_data': x_norm,
                'y_data': y_array,
                'x_mean': x_mean,
                'x_std': x_std,
                'crop_map': crop_map,
                'crop_map_inv': {v: k for k, v in crop_map.items()},
                'k': 5  # Number of neighbors to consider
            }
            
            # Save the model
            with open('crop_model.pkl', 'wb') as f:
                pickle.dump(self.model, f)
            
            logging.info(f"Trained model on {len(x_data)} samples with {len(crop_map)} different crops")
        except Exception as e:
            logging.error(f"Error training model: {str(e)}")
            raise
    
    def euclidean_distance(self, a, b):
        """Calculate Euclidean distance between two points"""
        return np.sqrt(np.sum((a - b) ** 2))
    
    def predict(self, n, p, k, temperature, humidity, ph, rainfall):
        """Predict the best crop based on soil parameters"""
        if self.model is None:
            raise ValueError("Model not initialized. Please train the model first.")
        
        # Create input feature vector
        x = np.array([n, p, k, temperature, humidity, ph, rainfall])
        
        # Normalize input
        x_norm = (x - self.model['x_mean']) / (self.model['x_std'] + 1e-8)
        
        # Calculate distances to all data points
        distances = []
        for i, sample in enumerate(self.model['x_data']):
            dist = self.euclidean_distance(x_norm, sample)
            distances.append((dist, i))
        
        # Sort by distance
        distances.sort()
        
        # Get the k nearest neighbors
        k = self.model['k']
        k_nearest = distances[:k]
        
        # Count the crops of the nearest neighbors
        crop_counts = defaultdict(int)
        for _, idx in k_nearest:
            crop_idx = self.model['y_data'][idx]
            crop_name = self.model['crop_map_inv'][crop_idx]
            crop_counts[crop_name] += 1
        
        # Calculate confidence scores
        total_neighbors = len(k_nearest)
        confidence_scores = {crop: (count / total_neighbors) * 100 for crop, count in crop_counts.items()}
        
        # Find the most common crop
        recommended_crop = max(crop_counts.items(), key=lambda x: x[1])[0]
        
        # Generate confidence scores for all known crops
        all_crop_confidence = {crop: 0 for crop in self.get_all_crops()}
        all_crop_confidence.update(confidence_scores)
        
        return recommended_crop, all_crop_confidence
    
    def get_optimal_conditions(self, crop_name):
        """Get optimal growing conditions for a specific crop"""
        if crop_name not in self.crop_data:
            raise ValueError(f"No data available for crop: {crop_name}")
        
        return self.crop_data[crop_name]
    
    def get_all_crops(self):
        """Get list of all available crops"""
        return list(self.crop_data.keys())
    
    def add_crop_data(self, crop_name, conditions):
        """Add a new crop or update an existing one"""
        self.crop_data[crop_name] = conditions
    
    def analyze_soil_health(self, n, p, k, ph):
        """Analyze soil health based on parameters"""
        health_score = 0
        recommendations = []
        
        # Check nitrogen levels
        if n < 30:
            health_score += 1
            recommendations.append("Low nitrogen levels. Consider adding nitrogen-rich fertilizers or compost.")
        elif n > 100:
            health_score += 2
            recommendations.append("High nitrogen levels. Consider planting nitrogen-depleting crops.")
        else:
            health_score += 3
        
        # Check phosphorus levels
        if p < 20:
            health_score += 1
            recommendations.append("Low phosphorus levels. Consider adding bone meal or rock phosphate.")
        elif p > 80:
            health_score += 2
            recommendations.append("High phosphorus levels. Avoid adding more phosphorus-rich fertilizers.")
        else:
            health_score += 3
        
        # Check potassium levels
        if k < 20:
            health_score += 1
            recommendations.append("Low potassium levels. Consider adding wood ash or potassium-rich fertilizers.")
        elif k > 80:
            health_score += 2
            recommendations.append("High potassium levels. Avoid adding more potassium-rich fertilizers.")
        else:
            health_score += 3
        
        # Check pH levels
        if ph < 5.5:
            health_score += 1
            recommendations.append("Soil is too acidic. Consider adding lime to raise pH.")
        elif ph > 7.5:
            health_score += 1
            recommendations.append("Soil is too alkaline. Consider adding sulfur to lower pH.")
        else:
            health_score += 3
        
        # Calculate overall health score (out of 100)
        health_percentage = (health_score / 12) * 100
        
        # Determine health category
        if health_percentage >= 75:
            health_category = "Good"
        elif health_percentage >= 50:
            health_category = "Moderate"
        else:
            health_category = "Poor"
        
        return {
            "score": health_percentage,
            "category": health_category,
            "recommendations": recommendations
        }
    
    def predict_yield(self, crop, n, p, k, temperature, humidity, ph, rainfall):
        """Predict potential yield percentage based on optimal vs. actual conditions"""
        try:
            if crop not in self.crop_data:
                return {
                    "success": False,
                    "error": f"No data available for crop: {crop}"
                }
            
            conditions = self.crop_data[crop]
            
            # Calculate how close each parameter is to the optimal range (0-100%)
            n_score = self.calculate_parameter_score(n, conditions['n_min'], conditions['n_max'])
            p_score = self.calculate_parameter_score(p, conditions['p_min'], conditions['p_max'])
            k_score = self.calculate_parameter_score(k, conditions['k_min'], conditions['k_max'])
            temp_score = self.calculate_parameter_score(temperature, conditions['temperature_min'], conditions['temperature_max'])
            humidity_score = self.calculate_parameter_score(humidity, conditions['humidity_min'], conditions['humidity_max'])
            ph_score = self.calculate_parameter_score(ph, conditions['ph_min'], conditions['ph_max'])
            rainfall_score = self.calculate_parameter_score(rainfall, conditions['rainfall_min'], conditions['rainfall_max'])
            
            # Calculate weighted average (give more weight to critical factors)
            weights = {
                'n': 0.15,
                'p': 0.15,
                'k': 0.15,
                'temperature': 0.15,
                'humidity': 0.1,
                'ph': 0.15,
                'rainfall': 0.15
            }
            
            weighted_score = (
                n_score * weights['n'] +
                p_score * weights['p'] +
                k_score * weights['k'] +
                temp_score * weights['temperature'] +
                humidity_score * weights['humidity'] +
                ph_score * weights['ph'] +
                rainfall_score * weights['rainfall']
            )
            
            # Calculate potential yield percentage
            yield_potential = weighted_score * 100
            
            # Determine limiting factors (parameters with lowest scores)
            parameter_scores = {
                'Nitrogen': n_score,
                'Phosphorus': p_score,
                'Potassium': k_score,
                'Temperature': temp_score,
                'Humidity': humidity_score,
                'pH': ph_score,
                'Rainfall': rainfall_score
            }
            
            limiting_factors = sorted(parameter_scores.items(), key=lambda x: x[1])[:2]
            
            return {
                "success": True,
                "yield_potential": yield_potential,
                "parameter_scores": parameter_scores,
                "limiting_factors": limiting_factors
            }
        except Exception as e:
            logging.error(f"Error predicting yield: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def calculate_parameter_score(self, value, min_val, max_val):
        """Calculate how close a parameter is to its optimal range (0-1)"""
        if value < min_val:
            # Below optimal range
            # The further below, the lower the score
            # Let's say if it's 50% below min, score is 0.5
            ratio = value / min_val
            return max(0, ratio)
        elif value > max_val:
            # Above optimal range
            # The further above, the lower the score
            # If it's 50% above max, score is 0.5
            ratio = max_val / value
            return max(0, ratio)
        else:
            # Within optimal range
            return 1.0
    
    def find_suitable_crops(self, n, p, k, temperature, humidity, ph, rainfall):
        """Find all suitable crops for given conditions and rank them"""
        suitable_crops = []
        
        for crop_name, conditions in self.crop_data.items():
            # Calculate match score for each parameter (0-1)
            n_score = self.calculate_parameter_score(n, conditions['n_min'], conditions['n_max'])
            p_score = self.calculate_parameter_score(p, conditions['p_min'], conditions['p_max'])
            k_score = self.calculate_parameter_score(k, conditions['k_min'], conditions['k_max'])
            temp_score = self.calculate_parameter_score(temperature, conditions['temperature_min'], conditions['temperature_max'])
            humidity_score = self.calculate_parameter_score(humidity, conditions['humidity_min'], conditions['humidity_max'])
            ph_score = self.calculate_parameter_score(ph, conditions['ph_min'], conditions['ph_max'])
            rainfall_score = self.calculate_parameter_score(rainfall, conditions['rainfall_min'], conditions['rainfall_max'])
            
            # Calculate overall match score (weighted average)
            weights = {
                'n': 0.15,
                'p': 0.15,
                'k': 0.15,
                'temperature': 0.15,
                'humidity': 0.1,
                'ph': 0.15,
                'rainfall': 0.15
            }
            
            overall_score = (
                n_score * weights['n'] +
                p_score * weights['p'] +
                k_score * weights['k'] +
                temp_score * weights['temperature'] +
                humidity_score * weights['humidity'] +
                ph_score * weights['ph'] +
                rainfall_score * weights['rainfall']
            ) * 100  # Convert to percentage
            
            suitable_crops.append({
                'crop': crop_name,
                'score': overall_score,
                'parameter_scores': {
                    'nitrogen': n_score * 100,
                    'phosphorus': p_score * 100,
                    'potassium': k_score * 100,
                    'temperature': temp_score * 100,
                    'humidity': humidity_score * 100,
                    'ph': ph_score * 100,
                    'rainfall': rainfall_score * 100
                }
            })
        
        # Sort by overall score (descending)
        suitable_crops.sort(key=lambda x: x['score'], reverse=True)
        
        return suitable_crops
