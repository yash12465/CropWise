import os
import requests
import json
import logging
from datetime import datetime, timedelta

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0"
        self.cache = {}  # Simple in-memory cache
        self.cache_duration = 3600  # Cache weather data for 1 hour
        
    def get_current_weather(self, location):
        """Get current weather for a location (city name, zip code, or coordinates)"""
        if not self.api_key:
            return {
                "success": False,
                "error": "Weather API key not configured. Please set the OPENWEATHERMAP_API_KEY."
            }
        
        # Check cache first
        cache_key = f"current_{location}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Determine if location is coordinates, zipcode, or city name
            if isinstance(location, tuple) and len(location) == 2:
                # Location is (lat, lon)
                lat, lon = location
                url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            elif isinstance(location, str) and (location.isdigit() or (location.startswith('+') and location[1:].isdigit())):
                # Location is a zip code
                url = f"{self.base_url}/weather?zip={location},us&appid={self.api_key}&units=metric"
            else:
                # Location is a city name
                url = f"{self.base_url}/weather?q={location}&appid={self.api_key}&units=metric"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Format the response data for our needs
                formatted_data = {
                    "success": True,
                    "location": {
                        "name": data.get("name", "Unknown"),
                        "country": data.get("sys", {}).get("country", "Unknown"),
                        "coordinates": {
                            "latitude": data.get("coord", {}).get("lat"),
                            "longitude": data.get("coord", {}).get("lon")
                        }
                    },
                    "weather": {
                        "temperature": {
                            "current": data.get("main", {}).get("temp"),
                            "feels_like": data.get("main", {}).get("feels_like"),
                            "min": data.get("main", {}).get("temp_min"),
                            "max": data.get("main", {}).get("temp_max")
                        },
                        "humidity": data.get("main", {}).get("humidity"),
                        "pressure": data.get("main", {}).get("pressure"),
                        "wind": {
                            "speed": data.get("wind", {}).get("speed"),
                            "direction": data.get("wind", {}).get("deg")
                        },
                        "clouds": data.get("clouds", {}).get("all"),
                        "description": data.get("weather", [{}])[0].get("description", ""),
                        "icon": data.get("weather", [{}])[0].get("icon", ""),
                        "timestamp": data.get("dt")
                    }
                }
                
                # If rain data exists, add it
                if "rain" in data:
                    formatted_data["weather"]["rainfall"] = {
                        "1h": data.get("rain", {}).get("1h", 0),
                        "3h": data.get("rain", {}).get("3h", 0)
                    }
                else:
                    formatted_data["weather"]["rainfall"] = {
                        "1h": 0,
                        "3h": 0
                    }
                
                # Cache the formatted data
                self._add_to_cache(cache_key, formatted_data)
                
                return formatted_data
            else:
                return {
                    "success": False,
                    "error": f"Error fetching weather data: {data.get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            logging.error(f"Weather API error: {str(e)}")
            return {
                "success": False,
                "error": f"Error connecting to weather service: {str(e)}"
            }
    
    def get_forecast(self, location, days=5):
        """Get weather forecast for a location for the specified number of days"""
        if not self.api_key:
            return {
                "success": False,
                "error": "Weather API key not configured. Please set the OPENWEATHERMAP_API_KEY."
            }
        
        # Check cache first
        cache_key = f"forecast_{location}_{days}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Determine if location is coordinates, zipcode, or city name
            if isinstance(location, tuple) and len(location) == 2:
                # Location is (lat, lon)
                lat, lon = location
                url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            elif isinstance(location, str) and (location.isdigit() or (location.startswith('+') and location[1:].isdigit())):
                # Location is a zip code
                url = f"{self.base_url}/forecast?zip={location},us&appid={self.api_key}&units=metric"
            else:
                # Location is a city name
                url = f"{self.base_url}/forecast?q={location}&appid={self.api_key}&units=metric"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # OpenWeatherMap forecast returns data in 3-hour intervals
                # Group by day and calculate daily averages
                daily_forecasts = {}
                location_info = {
                    "name": data.get("city", {}).get("name", "Unknown"),
                    "country": data.get("city", {}).get("country", "Unknown"),
                    "coordinates": {
                        "latitude": data.get("city", {}).get("coord", {}).get("lat"),
                        "longitude": data.get("city", {}).get("coord", {}).get("lon")
                    }
                }
                
                for forecast in data.get("list", []):
                    dt = datetime.fromtimestamp(forecast.get("dt"))
                    date_key = dt.strftime("%Y-%m-%d")
                    
                    if date_key not in daily_forecasts:
                        daily_forecasts[date_key] = {
                            "date": date_key,
                            "temperatures": [],
                            "humidity": [],
                            "rainfall": [],
                            "wind_speed": [],
                            "descriptions": [],
                            "icons": []
                        }
                    
                    daily_forecasts[date_key]["temperatures"].append(forecast.get("main", {}).get("temp"))
                    daily_forecasts[date_key]["humidity"].append(forecast.get("main", {}).get("humidity"))
                    
                    # Extract rainfall if available
                    if "rain" in forecast and "3h" in forecast["rain"]:
                        daily_forecasts[date_key]["rainfall"].append(forecast["rain"]["3h"])
                    else:
                        daily_forecasts[date_key]["rainfall"].append(0)
                    
                    daily_forecasts[date_key]["wind_speed"].append(forecast.get("wind", {}).get("speed"))
                    daily_forecasts[date_key]["descriptions"].append(forecast.get("weather", [{}])[0].get("description", ""))
                    daily_forecasts[date_key]["icons"].append(forecast.get("weather", [{}])[0].get("icon", ""))
                
                # Calculate daily averages and get most common description and icon
                forecast_days = []
                for date_key in sorted(daily_forecasts.keys())[:days]:
                    day_data = daily_forecasts[date_key]
                    
                    # Find most common description and icon
                    description_counts = {}
                    icon_counts = {}
                    for desc in day_data["descriptions"]:
                        description_counts[desc] = description_counts.get(desc, 0) + 1
                    for icon in day_data["icons"]:
                        icon_counts[icon] = icon_counts.get(icon, 0) + 1
                    
                    most_common_description = max(description_counts.items(), key=lambda x: x[1])[0]
                    most_common_icon = max(icon_counts.items(), key=lambda x: x[1])[0]
                    
                    forecast_days.append({
                        "date": day_data["date"],
                        "temperature": {
                            "avg": sum(day_data["temperatures"]) / len(day_data["temperatures"]),
                            "min": min(day_data["temperatures"]),
                            "max": max(day_data["temperatures"])
                        },
                        "humidity": sum(day_data["humidity"]) / len(day_data["humidity"]),
                        "rainfall": sum(day_data["rainfall"]),
                        "wind_speed": sum(day_data["wind_speed"]) / len(day_data["wind_speed"]),
                        "description": most_common_description,
                        "icon": most_common_icon
                    })
                
                formatted_data = {
                    "success": True,
                    "location": location_info,
                    "forecast": forecast_days
                }
                
                # Cache the formatted data
                self._add_to_cache(cache_key, formatted_data)
                
                return formatted_data
            else:
                return {
                    "success": False,
                    "error": f"Error fetching forecast data: {data.get('message', 'Unknown error')}"
                }
                
        except Exception as e:
            logging.error(f"Weather API forecast error: {str(e)}")
            return {
                "success": False,
                "error": f"Error connecting to weather service: {str(e)}"
            }
    
    def get_location_coordinates(self, location_name):
        """Convert a location name to coordinates using Geocoding API"""
        if not self.api_key:
            return None
        
        try:
            url = f"{self.geo_url}/direct?q={location_name}&limit=1&appid={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return (data[0].get("lat"), data[0].get("lon"))
            
            return None
        except Exception as e:
            logging.error(f"Geocoding API error: {str(e)}")
            return None
    
    def _add_to_cache(self, key, data):
        """Add data to cache with expiration time"""
        self.cache[key] = {
            "data": data,
            "expires": datetime.now() + timedelta(seconds=self.cache_duration)
        }
    
    def _get_from_cache(self, key):
        """Get data from cache if not expired"""
        if key in self.cache:
            cache_item = self.cache[key]
            if datetime.now() < cache_item["expires"]:
                return cache_item["data"]
            else:
                # Remove expired item
                del self.cache[key]
        
        return None

# Initialize the weather service when the module is imported
weather_service = WeatherService()