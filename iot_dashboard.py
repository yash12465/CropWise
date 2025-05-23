import os
import json
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path
import math

class IoTSensorManager:
    """Manage IoT sensor data for smart farming"""
    
    def __init__(self):
        """Initialize the IoT sensor manager"""
        self.sensor_data = self._load_sensor_data()
        self.sensor_types = {
            "soil_moisture": {"unit": "%", "optimal_range": [30, 70]},
            "soil_temperature": {"unit": "°C", "optimal_range": [20, 35]},
            "soil_ph": {"unit": "pH", "optimal_range": [5.5, 7.5]},
            "soil_npk": {"unit": "ppm", "optimal_range": [100, 200]},
            "air_temperature": {"unit": "°C", "optimal_range": [18, 32]},
            "humidity": {"unit": "%", "optimal_range": [40, 80]},
            "light_intensity": {"unit": "lux", "optimal_range": [10000, 50000]},
            "water_level": {"unit": "%", "optimal_range": [60, 90]},
        }
        
    def _load_sensor_data(self):
        """Load sensor data from file or create if it doesn't exist"""
        try:
            data_path = Path("iot_sensor_data.json")
            
            if data_path.exists():
                with open(data_path, "r") as f:
                    return json.load(f)
            else:
                # Create default sensor data
                default_data = self._create_default_sensor_data()
                with open(data_path, "w") as f:
                    json.dump(default_data, f, indent=2)
                return default_data
        except Exception as e:
            logging.error(f"Error loading sensor data: {str(e)}")
            return self._create_default_sensor_data()
            
    def _create_default_sensor_data(self):
        """Create default sensor data for demonstration"""
        # Generate timestamps for the last 24 hours
        now = datetime.now()
        timestamps = [(now - timedelta(hours=i)).isoformat() for i in range(24, 0, -1)]
        
        # Generate some simulated sensor data
        return {
            "farm_1": {
                "name": "Main Farm",
                "location": "Pune, Maharashtra",
                "size_hectares": 5.2,
                "active_sensors": ["soil_moisture", "soil_temperature", "soil_ph", "air_temperature", "humidity"],
                "crops": ["wheat", "cotton"],
                "sensor_readings": {
                    "soil_moisture": self._generate_readings(timestamps, 45, 10, [30, 70]),
                    "soil_temperature": self._generate_readings(timestamps, 25, 3, [20, 35]),
                    "soil_ph": self._generate_readings(timestamps, 6.5, 0.3, [5.5, 7.5]),
                    "air_temperature": self._generate_readings(timestamps, 28, 5, [18, 32]),
                    "humidity": self._generate_readings(timestamps, 60, 15, [40, 80])
                }
            },
            "farm_2": {
                "name": "River Field",
                "location": "Ambala, Haryana",
                "size_hectares": 3.8,
                "active_sensors": ["soil_moisture", "soil_npk", "water_level", "soil_temperature"],
                "crops": ["rice", "maize"],
                "sensor_readings": {
                    "soil_moisture": self._generate_readings(timestamps, 55, 8, [30, 70]),
                    "soil_npk": self._generate_readings(timestamps, 150, 30, [100, 200]),
                    "water_level": self._generate_readings(timestamps, 75, 10, [60, 90]),
                    "soil_temperature": self._generate_readings(timestamps, 27, 2, [20, 35])
                }
            }
        }
        
    def _generate_readings(self, timestamps, mean, variation, optimal_range):
        """Generate simulated sensor readings with some variation"""
        readings = []
        value = mean
        
        # Add some seasonality
        for i, timestamp in enumerate(timestamps):
            # Add some random variation
            random_change = random.uniform(-variation, variation)
            
            # Add some time-based variation (daily cycle)
            hour = datetime.fromisoformat(timestamp).hour
            daily_variation = math.sin(hour / 24 * 2 * math.pi) * variation / 2
            
            # Combine variations
            new_value = value + random_change + daily_variation
            
            # Ensure values stay reasonably within range
            if i > 0 and abs(new_value - readings[-1]["value"]) > variation:
                new_value = readings[-1]["value"] + random.uniform(-variation/2, variation/2)
                
            # Status based on optimal range
            status = "normal"
            if new_value < optimal_range[0]:
                status = "low"
            elif new_value > optimal_range[1]:
                status = "high"
                
            readings.append({
                "timestamp": timestamp,
                "value": round(new_value, 2),
                "status": status
            })
            
            # Slightly adjust the next base value for some trend
            value += random.uniform(-variation/4, variation/4)
            
        return readings
        
    def get_farm_list(self):
        """Get a list of all farms with active sensors"""
        farm_list = []
        for farm_id, farm_data in self.sensor_data.items():
            farm_list.append({
                "id": farm_id,
                "name": farm_data["name"],
                "location": farm_data["location"],
                "size_hectares": farm_data["size_hectares"],
                "active_sensors": farm_data["active_sensors"],
                "crops": farm_data["crops"]
            })
        return farm_list
        
    def get_farm_data(self, farm_id):
        """Get detailed data for a specific farm"""
        if farm_id not in self.sensor_data:
            return None
        return self.sensor_data[farm_id]
        
    def get_latest_readings(self, farm_id):
        """Get the latest sensor readings for a farm"""
        if farm_id not in self.sensor_data:
            return None
            
        farm = self.sensor_data[farm_id]
        latest_readings = {}
        
        for sensor_type, readings in farm["sensor_readings"].items():
            if readings:
                latest_readings[sensor_type] = readings[-1]
                latest_readings[sensor_type]["unit"] = self.sensor_types[sensor_type]["unit"]
                latest_readings[sensor_type]["optimal_range"] = self.sensor_types[sensor_type]["optimal_range"]
                
        return latest_readings
        
    def get_historical_data(self, farm_id, sensor_type, period="24h"):
        """Get historical sensor data for a specific period"""
        if farm_id not in self.sensor_data or sensor_type not in self.sensor_data[farm_id]["sensor_readings"]:
            return None
            
        readings = self.sensor_data[farm_id]["sensor_readings"][sensor_type]
        
        # For now, just return all data (which is 24h in our demo)
        # In a real system, we would filter based on the period
        return {
            "sensor_type": sensor_type,
            "unit": self.sensor_types[sensor_type]["unit"],
            "optimal_range": self.sensor_types[sensor_type]["optimal_range"],
            "readings": readings
        }
        
    def add_sensor_reading(self, farm_id, sensor_type, value):
        """Add a new sensor reading (would be called by actual IoT devices)"""
        if farm_id not in self.sensor_data or sensor_type not in self.sensor_types:
            return False
            
        if sensor_type not in self.sensor_data[farm_id]["sensor_readings"]:
            self.sensor_data[farm_id]["sensor_readings"][sensor_type] = []
            
        # Determine status based on optimal range
        status = "normal"
        if value < self.sensor_types[sensor_type]["optimal_range"][0]:
            status = "low"
        elif value > self.sensor_types[sensor_type]["optimal_range"][1]:
            status = "high"
            
        # Add the new reading
        self.sensor_data[farm_id]["sensor_readings"][sensor_type].append({
            "timestamp": datetime.now().isoformat(),
            "value": value,
            "status": status
        })
        
        # Limit to last 100 readings
        if len(self.sensor_data[farm_id]["sensor_readings"][sensor_type]) > 100:
            self.sensor_data[farm_id]["sensor_readings"][sensor_type] = self.sensor_data[farm_id]["sensor_readings"][sensor_type][-100:]
            
        # Save updated data
        try:
            with open("iot_sensor_data.json", "w") as f:
                json.dump(self.sensor_data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving sensor data: {str(e)}")
            return False
            
        return True
        
    def generate_alert(self, farm_id, sensor_type, reading):
        """Generate alert based on sensor reading"""
        if sensor_type not in self.sensor_types:
            return None
            
        optimal_range = self.sensor_types[sensor_type]["optimal_range"]
        unit = self.sensor_types[sensor_type]["unit"]
        value = reading["value"]
        
        if value < optimal_range[0]:
            severity = "warning" if value > optimal_range[0] * 0.8 else "critical"
            action = self._get_action_recommendation(sensor_type, "low")
            return {
                "severity": severity,
                "message": f"Low {sensor_type.replace('_', ' ')} detected: {value}{unit} (optimal: {optimal_range[0]}-{optimal_range[1]}{unit})",
                "recommended_action": action
            }
        elif value > optimal_range[1]:
            severity = "warning" if value < optimal_range[1] * 1.2 else "critical"
            action = self._get_action_recommendation(sensor_type, "high")
            return {
                "severity": severity,
                "message": f"High {sensor_type.replace('_', ' ')} detected: {value}{unit} (optimal: {optimal_range[0]}-{optimal_range[1]}{unit})",
                "recommended_action": action
            }
            
        return None
        
    def get_farm_alerts(self, farm_id):
        """Get all current alerts for a farm based on latest readings"""
        if farm_id not in self.sensor_data:
            return []
            
        latest_readings = self.get_latest_readings(farm_id)
        alerts = []
        
        for sensor_type, reading in latest_readings.items():
            alert = self.generate_alert(farm_id, sensor_type, reading)
            if alert:
                alert["sensor_type"] = sensor_type
                alert["timestamp"] = reading["timestamp"]
                alerts.append(alert)
                
        return alerts
        
    def _get_action_recommendation(self, sensor_type, condition):
        """Get recommended action based on sensor type and condition"""
        recommendations = {
            "soil_moisture": {
                "low": "Increase irrigation. Consider checking irrigation system for blockages or inefficiencies.",
                "high": "Reduce irrigation. Ensure proper drainage and consider postponing any scheduled irrigation."
            },
            "soil_temperature": {
                "low": "Consider using mulch to insulate soil. For sensitive crops, temporary covers may be needed.",
                "high": "Apply mulch to cool soil. Ensure adequate irrigation and consider shade for sensitive crops."
            },
            "soil_ph": {
                "low": "Soil is acidic. Consider applying agricultural lime to raise pH level.",
                "high": "Soil is alkaline. Consider adding organic matter or sulfur-based amendments to lower pH."
            },
            "soil_npk": {
                "low": "Nutrient deficiency detected. Apply balanced NPK fertilizer according to crop requirements.",
                "high": "Excess nutrients detected. Avoid further fertilization and monitor for nutrient runoff."
            },
            "air_temperature": {
                "low": "Low air temperature. Monitor crops for cold stress and consider protective measures.",
                "high": "High air temperature. Ensure adequate irrigation and consider temporary shading."
            },
            "humidity": {
                "low": "Low humidity may cause water stress. Consider increasing irrigation frequency.",
                "high": "High humidity increases disease risk. Improve ventilation and monitor for fungal diseases."
            },
            "light_intensity": {
                "low": "Low light levels may affect photosynthesis. Consider pruning surrounding vegetation.",
                "high": "High light levels may cause sunscald. Consider partial shading for sensitive crops."
            },
            "water_level": {
                "low": "Water reservoir level is low. Refill water storage or adjust irrigation schedule.",
                "high": "Water level too high. Check for proper drainage and potential flooding risks."
            }
        }
        
        if sensor_type in recommendations and condition in recommendations[sensor_type]:
            return recommendations[sensor_type][condition]
        
        return "Monitor conditions and take appropriate action based on crop requirements."


# Initialize the IoT sensor manager
iot_manager = IoTSensorManager()