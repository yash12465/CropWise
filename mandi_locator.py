import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import random

class MandiLocator:
    """Locate and track local mandis (agricultural markets) in India"""
    
    def __init__(self):
        """Initialize the mandi locator with market data"""
        self.mandi_data = self._load_mandi_data()
        
    def _load_mandi_data(self):
        """Load mandi data from file or create if it doesn't exist"""
        try:
            data_path = Path("mandi_data.json")
            
            if data_path.exists():
                with open(data_path, "r") as f:
                    return json.load(f)
            else:
                # Create default mandi data
                default_data = self._create_default_mandi_data()
                with open(data_path, "w") as f:
                    json.dump(default_data, f, indent=2)
                return default_data
        except Exception as e:
            logging.error(f"Error loading mandi data: {str(e)}")
            return self._create_default_mandi_data()
            
    def _create_default_mandi_data(self):
        """Create default mandi data for major agricultural markets in India"""
        today = datetime.now()
        
        return {
            "states": [
                {
                    "name": "Maharashtra",
                    "mandis": [
                        {
                            "id": "mh_pune",
                            "name": "Pune Agricultural Produce Market",
                            "location": {
                                "district": "Pune", 
                                "address": "Market Yard, Gultekdi, Pune",
                                "coordinates": {"lat": 18.4919, "lng": 73.8656}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "6:00 AM - 7:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport", "Banking"],
                            "contact": {
                                "phone": "020-24261957",
                                "email": "puneapmc@example.com"
                            },
                            "commodities": ["Wheat", "Rice", "Jowar", "Vegetables", "Fruits"],
                            "current_prices": {
                                "Wheat": self._generate_price_data(22.50, 2.5, 7, today),
                                "Rice": self._generate_price_data(35.80, 3.2, 7, today),
                                "Onions": self._generate_price_data(18.40, 5.8, 7, today),
                                "Tomatoes": self._generate_price_data(24.60, 8.5, 7, today)
                            }
                        },
                        {
                            "id": "mh_nashik",
                            "name": "Nashik Agricultural Market Committee",
                            "location": {
                                "district": "Nashik", 
                                "address": "APMC Market, Nashik",
                                "coordinates": {"lat": 19.9975, "lng": 73.7898}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "7:00 AM - 6:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport"],
                            "contact": {
                                "phone": "0253-2465936",
                                "email": "nashikapmc@example.com"
                            },
                            "commodities": ["Grapes", "Onions", "Tomatoes", "Wheat"],
                            "current_prices": {
                                "Grapes": self._generate_price_data(65.40, 12.5, 7, today),
                                "Onions": self._generate_price_data(16.80, 4.8, 7, today),
                                "Wheat": self._generate_price_data(21.90, 2.2, 7, today)
                            }
                        }
                    ]
                },
                {
                    "name": "Punjab",
                    "mandis": [
                        {
                            "id": "pb_ludhiana",
                            "name": "Ludhiana Grain Market",
                            "location": {
                                "district": "Ludhiana", 
                                "address": "Grain Market, Gill Road, Ludhiana",
                                "coordinates": {"lat": 30.9010, "lng": 75.8573}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "6:00 AM - 8:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport", "Banking", "Farmers Rest House"],
                            "contact": {
                                "phone": "0161-2524935",
                                "email": "ludhianaapmc@example.com"
                            },
                            "commodities": ["Wheat", "Rice", "Maize", "Cotton"],
                            "current_prices": {
                                "Wheat": self._generate_price_data(23.80, 2.1, 7, today),
                                "Rice": self._generate_price_data(36.50, 3.0, 7, today),
                                "Maize": self._generate_price_data(18.20, 2.5, 7, today),
                                "Cotton": self._generate_price_data(70.40, 8.5, 7, today)
                            }
                        }
                    ]
                },
                {
                    "name": "Uttar Pradesh",
                    "mandis": [
                        {
                            "id": "up_kanpur",
                            "name": "Kanpur Agricultural Market",
                            "location": {
                                "district": "Kanpur", 
                                "address": "APMC Market, Kanpur",
                                "coordinates": {"lat": 26.4499, "lng": 80.3319}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "7:00 AM - 7:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport"],
                            "contact": {
                                "phone": "0512-2546789",
                                "email": "kanpurapmc@example.com"
                            },
                            "commodities": ["Wheat", "Rice", "Pulses", "Vegetables"],
                            "current_prices": {
                                "Wheat": self._generate_price_data(21.60, 2.3, 7, today),
                                "Rice": self._generate_price_data(34.20, 3.5, 7, today),
                                "Pulses": self._generate_price_data(85.40, 10.5, 7, today)
                            }
                        }
                    ]
                },
                {
                    "name": "Karnataka",
                    "mandis": [
                        {
                            "id": "ka_bangalore",
                            "name": "Bangalore APMC Yard",
                            "location": {
                                "district": "Bangalore", 
                                "address": "Yeshwanthpur APMC Yard, Bangalore",
                                "coordinates": {"lat": 13.0035, "lng": 77.5721}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "6:00 AM - 7:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport", "Banking", "E-trading"],
                            "contact": {
                                "phone": "080-23472275",
                                "email": "bangaloreapmc@example.com"
                            },
                            "commodities": ["Ragi", "Rice", "Pulses", "Vegetables", "Fruits"],
                            "current_prices": {
                                "Ragi": self._generate_price_data(28.40, 3.5, 7, today),
                                "Rice": self._generate_price_data(38.20, 4.2, 7, today),
                                "Tomatoes": self._generate_price_data(32.50, 12.5, 7, today),
                                "Mangoes": self._generate_price_data(120.40, 25.5, 7, today)
                            }
                        }
                    ]
                },
                {
                    "name": "Gujarat",
                    "mandis": [
                        {
                            "id": "gu_ahmedabad",
                            "name": "Ahmedabad Market Yard",
                            "location": {
                                "district": "Ahmedabad", 
                                "address": "APMC Market Yard, Ahmedabad",
                                "coordinates": {"lat": 23.0305, "lng": 72.5581}
                            },
                            "open_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            "market_hours": "7:00 AM - 7:00 PM",
                            "facilities": ["Storage", "Weighing", "Transport", "E-trading"],
                            "contact": {
                                "phone": "079-27542653",
                                "email": "ahmedabadapmc@example.com"
                            },
                            "commodities": ["Cotton", "Groundnut", "Wheat", "Vegetables"],
                            "current_prices": {
                                "Cotton": self._generate_price_data(75.60, 8.2, 7, today),
                                "Groundnut": self._generate_price_data(54.30, 6.5, 7, today),
                                "Wheat": self._generate_price_data(22.40, 2.4, 7, today)
                            }
                        }
                    ]
                }
            ],
            "last_updated": today.isoformat()
        }

    def _generate_price_data(self, base_price, variation, days, end_date):
        """Generate simulated price data for the last several days"""
        price_data = []
        current_price = base_price
        
        for i in range(days, 0, -1):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            
            # Add some random variation day to day
            change = random.uniform(-variation/2, variation/2)
            current_price += change
            
            # Ensure price doesn't go below reasonable value
            current_price = max(current_price, base_price * 0.7)
            
            price_data.append({
                "date": date,
                "price": round(current_price, 2)
            })
            
        return price_data
        
    def get_states_list(self):
        """Get list of all states with mandis"""
        return [state["name"] for state in self.mandi_data["states"]]
        
    def get_mandis_by_state(self, state_name):
        """Get all mandis in a state"""
        for state in self.mandi_data["states"]:
            if state["name"].lower() == state_name.lower():
                return state["mandis"]
        return []
        
    def get_mandis_by_crop(self, crop_name):
        """Get all mandis that trade a specific crop"""
        matching_mandis = []
        
        for state in self.mandi_data["states"]:
            for mandi in state["mandis"]:
                if crop_name.lower() in [c.lower() for c in mandi["commodities"]]:
                    mandi_copy = mandi.copy()
                    mandi_copy["state"] = state["name"]
                    matching_mandis.append(mandi_copy)
                    
        return matching_mandis
        
    def get_mandi_details(self, mandi_id):
        """Get detailed information about a specific mandi"""
        for state in self.mandi_data["states"]:
            for mandi in state["mandis"]:
                if mandi["id"] == mandi_id:
                    mandi_copy = mandi.copy()
                    mandi_copy["state"] = state["name"]
                    return mandi_copy
        return None
        
    def get_nearby_mandis(self, lat, lng, radius_km=50):
        """Find mandis within a certain radius of coordinates"""
        # In a production system, we would use proper geospatial queries
        # For this demo, we'll use a simplified calculation
        nearby_mandis = []
        
        for state in self.mandi_data["states"]:
            for mandi in state["mandis"]:
                mandi_lat = mandi["location"]["coordinates"]["lat"]
                mandi_lng = mandi["location"]["coordinates"]["lng"]
                
                # Calculate approximate distance (very rough estimate)
                # In production, use proper haversine formula or geo library
                distance = ((lat - mandi_lat) ** 2 + (lng - mandi_lng) ** 2) ** 0.5 * 111  # rough km conversion
                
                if distance <= radius_km:
                    mandi_copy = mandi.copy()
                    mandi_copy["state"] = state["name"]
                    mandi_copy["distance_km"] = round(distance, 1)
                    nearby_mandis.append(mandi_copy)
                    
        return nearby_mandis
        
    def get_price_trends(self, mandi_id, commodity):
        """Get price trends for a specific commodity at a mandi"""
        mandi = self.get_mandi_details(mandi_id)
        
        if not mandi or commodity not in mandi["current_prices"]:
            return None
            
        price_data = mandi["current_prices"][commodity]
        
        # Calculate some trend statistics
        if len(price_data) > 1:
            first_price = price_data[0]["price"]
            last_price = price_data[-1]["price"]
            price_change = last_price - first_price
            percent_change = (price_change / first_price) * 100
            
            return {
                "commodity": commodity,
                "mandi": mandi["name"],
                "location": mandi["location"]["district"],
                "state": mandi["state"],
                "current_price": last_price,
                "price_change": round(price_change, 2),
                "percent_change": round(percent_change, 2),
                "trend": "up" if price_change > 0 else "down",
                "price_data": price_data
            }
            
        return None
        
    def compare_prices(self, commodity, state=None):
        """Compare prices for a commodity across different mandis"""
        results = []
        
        for state_data in self.mandi_data["states"]:
            if state and state_data["name"].lower() != state.lower():
                continue
                
            for mandi in state_data["mandis"]:
                if commodity in mandi["current_prices"]:
                    price_data = mandi["current_prices"][commodity]
                    if price_data:
                        current_price = price_data[-1]["price"]
                        results.append({
                            "mandi_id": mandi["id"],
                            "mandi_name": mandi["name"],
                            "district": mandi["location"]["district"],
                            "state": state_data["name"],
                            "price": current_price
                        })
                        
        # Sort by price
        results.sort(key=lambda x: x["price"])
        return results


# Initialize the mandi locator system
mandi_locator = MandiLocator()