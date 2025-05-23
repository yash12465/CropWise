import os
import json
import base64
import logging
from pathlib import Path

class ImagePestDetector:
    """A class for identifying crop pests and diseases based on image analysis"""
    
    def __init__(self):
        """Initialize the pest and disease detector with the default database"""
        self.pest_disease_db = self._load_pest_disease_database()
        self.image_features_db = self._load_image_features_database()
        
    def _load_pest_disease_database(self):
        """Load pest and disease database from JSON file"""
        try:
            database_path = Path("pest_disease_database.json")
            
            if database_path.exists():
                with open(database_path, "r") as f:
                    return json.load(f)
            else:
                # Create default database if it doesn't exist
                default_db = self._create_default_database()
                with open(database_path, "w") as f:
                    json.dump(default_db, f, indent=2)
                return default_db
        except Exception as e:
            logging.error(f"Error loading pest and disease database: {str(e)}")
            return self._create_default_database()

    def _load_image_features_database(self):
        """Load image features database if available"""
        try:
            database_path = Path("pest_disease_image_features.json")
            
            if database_path.exists():
                with open(database_path, "r") as f:
                    return json.load(f)
            else:
                # Create default image features database
                default_db = self._create_default_image_features()
                with open(database_path, "w") as f:
                    json.dump(default_db, f, indent=2)
                return default_db
        except Exception as e:
            logging.error(f"Error loading image features database: {str(e)}")
            return self._create_default_image_features()
            
    def _create_default_database(self):
        """Create a default pest and disease database"""
        return {
            "rice": {
                "pests": [
                    {
                        "name": "Rice Stem Borer",
                        "symptoms": ["White earheads", "Dead heart", "Holes in stems", "Yellowing leaves"],
                        "description": "Adult moths lay eggs on leaf tips. Larvae bore into stems, causing dead heart or white earheads.",
                        "treatment": "Use of Trichogramma parasitoids, neem-based sprays, or systemic insecticides like Carbofuran.",
                        "prevention": "Early planting, balanced fertilization, removal of stubble after harvest."
                    },
                    {
                        "name": "Brown Planthopper",
                        "symptoms": ["Yellowing leaves", "Hopperburn", "Stunted growth", "Honeydew on leaves"],
                        "description": "Small brown insects that suck sap from the base of the plant, causing plants to wilt and die.",
                        "treatment": "Buprofezin, Imidacloprid, or neem oil-based sprays.",
                        "prevention": "Avoid excessive nitrogenous fertilizers, maintain field sanitation, use resistant varieties."
                    }
                ],
                "diseases": [
                    {
                        "name": "Rice Blast",
                        "symptoms": ["Diamond-shaped lesions", "White to gray spots with dark borders", "Broken panicles"],
                        "description": "Fungal disease caused by Magnaporthe oryzae, affecting all above-ground parts of the rice plant.",
                        "treatment": "Apply fungicides like Tricyclazole, Isoprothiolane, or Carbendazim.",
                        "prevention": "Use resistant varieties, balanced fertilization, proper spacing, seed treatment."
                    },
                    {
                        "name": "Bacterial Leaf Blight",
                        "symptoms": ["Water-soaked lesions", "Yellow margins", "Wilting leaves", "Leaf curling"],
                        "description": "Bacterial disease that causes wilting of seedlings and yellowing and drying of leaves.",
                        "treatment": "Copper-based bactericides, streptomycin sulfate + tetracycline combination.",
                        "prevention": "Use disease-free seeds, resistant varieties, avoid overhead irrigation, maintain field sanitation."
                    }
                ]
            },
            "wheat": {
                "pests": [
                    {
                        "name": "Aphids",
                        "symptoms": ["Curled leaves", "Yellowing", "Stunted growth", "Honeydew on leaves"],
                        "description": "Small soft-bodied insects that suck plant sap, causing distortion and stunting.",
                        "treatment": "Insecticidal soaps, neem oil, or systemic insecticides like Imidacloprid.",
                        "prevention": "Encourage natural predators, maintain proper spacing, early sowing."
                    }
                ],
                "diseases": [
                    {
                        "name": "Wheat Rust",
                        "symptoms": ["Reddish-brown pustules", "Yellow to brown spots", "Infected stems", "Early senescence"],
                        "description": "Fungal disease that appears as rusty spots on leaves and stems, reducing photosynthesis.",
                        "treatment": "Fungicides containing Propiconazole, Tebuconazole, or Azoxystrobin.",
                        "prevention": "Use resistant varieties, early sowing, balanced fertilization, crop rotation."
                    },
                    {
                        "name": "Powdery Mildew",
                        "symptoms": ["White powdery patches", "Yellowing leaves", "Reduced vigor", "Premature drying"],
                        "description": "Fungal disease that appears as a white powdery coating on leaves and spikes.",
                        "treatment": "Sulfur-based fungicides, Triadimefon, or Propiconazole.",
                        "prevention": "Proper spacing, resistant varieties, balanced nitrogen application."
                    }
                ]
            },
            "cotton": {
                "pests": [
                    {
                        "name": "Pink Bollworm",
                        "symptoms": ["Rosette flowers", "Damaged bolls", "Pink larvae inside bolls", "Premature boll opening"],
                        "description": "Small pinkish-white caterpillars that feed inside cotton bolls, damaging fibers and seeds.",
                        "treatment": "Bt cotton varieties, pheromone traps, insecticides like Spinosad or Emamectin benzoate.",
                        "prevention": "Early sowing, timely harvest, destruction of crop residues, crop rotation."
                    },
                    {
                        "name": "Cotton Aphid",
                        "symptoms": ["Curled leaves", "Honeydew", "Sooty mold", "Stunted growth"],
                        "description": "Small soft-bodied insects that suck sap from leaves and stems.",
                        "treatment": "Neem oil, insecticidal soaps, systemic insecticides like Imidacloprid or Thiamethoxam.",
                        "prevention": "Balanced fertilization, encourage natural predators, proper spacing."
                    }
                ],
                "diseases": [
                    {
                        "name": "Cotton Leaf Curl Virus",
                        "symptoms": ["Upward curling of leaves", "Vein thickening", "Leaf enations", "Stunted growth"],
                        "description": "Viral disease transmitted by whiteflies, causing significant yield losses.",
                        "treatment": "No direct cure. Control whitefly vectors using appropriate insecticides.",
                        "prevention": "Use resistant varieties, control whiteflies, early sowing, crop rotation."
                    }
                ]
            },
            "tomato": {
                "pests": [
                    {
                        "name": "Tomato Fruit Borer",
                        "symptoms": ["Entry holes in fruits", "Damaged fruits", "Frass near entry points", "Caterpillars inside fruits"],
                        "description": "Also known as Helicoverpa armigera, this pest bores into fruits causing direct damage.",
                        "treatment": "Bt sprays, Neem extracts, or insecticides like Spinosad or Indoxacarb.",
                        "prevention": "Regular monitoring, pheromone traps, timely harvesting, crop rotation."
                    }
                ],
                "diseases": [
                    {
                        "name": "Early Blight",
                        "symptoms": ["Dark brown spots with concentric rings", "Yellowing around spots", "Lower leaf infection", "Premature defoliation"],
                        "description": "Fungal disease caused by Alternaria solani, primarily affecting older leaves.",
                        "treatment": "Fungicides containing Mancozeb, Chlorothalonil, or Azoxystrobin.",
                        "prevention": "Crop rotation, proper spacing, avoid overhead irrigation, remove infected leaves."
                    },
                    {
                        "name": "Late Blight",
                        "symptoms": ["Water-soaked lesions", "White fuzzy growth", "Rapid leaf death", "Brown lesions on fruits"],
                        "description": "Devastating fungal disease caused by Phytophthora infestans, can destroy entire crops.",
                        "treatment": "Copper-based fungicides, Mancozeb, or systemic fungicides like Metalaxyl+Mancozeb.",
                        "prevention": "Resistant varieties, proper spacing, avoid wet foliage, destroy volunteer plants."
                    }
                ]
            }
        }

    def _create_default_image_features(self):
        """Create default image features for common pests and diseases"""
        # In a real system, this would contain feature vectors extracted from pest and disease images
        # For now, we'll use a simplified representation
        return {
            "rice": {
                "Rice Blast": {
                    "visual_features": ["diamond lesions", "gray center", "brown border", "leaf spots"],
                    "color_patterns": ["gray", "brown", "tan"],
                    "texture_features": ["necrotic tissue", "dry patches"]
                },
                "Bacterial Leaf Blight": {
                    "visual_features": ["yellow margins", "water-soaked lesions", "wavy edges"],
                    "color_patterns": ["yellow", "green", "gray"],
                    "texture_features": ["wet appearance", "translucent edges"]
                },
                "Rice Stem Borer": {
                    "visual_features": ["white earheads", "dried central leaf", "holes in stem"],
                    "color_patterns": ["white", "yellow", "brown"],
                    "texture_features": ["hollow stems", "broken panicles"]
                }
            },
            "wheat": {
                "Wheat Rust": {
                    "visual_features": ["orange pustules", "raised spots", "linear patterns"],
                    "color_patterns": ["orange", "brown", "yellow"],
                    "texture_features": ["powdery", "raised lesions"]
                },
                "Powdery Mildew": {
                    "visual_features": ["white patches", "powdery coating", "even distribution"],
                    "color_patterns": ["white", "gray", "yellow background"],
                    "texture_features": ["powdery", "fuzzy coating", "superficial"]
                }
            },
            "tomato": {
                "Early Blight": {
                    "visual_features": ["concentric rings", "angular spots", "lower leaf damage"],
                    "color_patterns": ["brown", "yellow", "dark brown"],
                    "texture_features": ["dry", "papery", "target-like"]
                },
                "Late Blight": {
                    "visual_features": ["irregular green-black lesions", "white fuzzy growth", "large patches"],
                    "color_patterns": ["dark green", "black", "white"],
                    "texture_features": ["water-soaked", "fuzzy", "greasy"]
                }
            }
        }
        
    def analyze_image(self, crop_name, image_data):
        """
        Analyze an image to detect pests or diseases
        
        Args:
            crop_name: Name of the crop in the image
            image_data: Base64 encoded image data
            
        Returns:
            Dictionary with identified pests/diseases and confidence scores
        """
        # In a production system, this would use computer vision / machine learning
        # to analyze the image and identify pests/diseases
        
        try:
            # For now, we'll return a simulated response
            # This would normally be determined by analyzing the image
            
            if crop_name.lower() not in self.pest_disease_db:
                return {
                    "success": False,
                    "error": f"Crop '{crop_name}' not found in database"
                }
                
            crop_issues = self.pest_disease_db[crop_name.lower()]
            
            # For demonstration purposes only - would be replaced by actual image analysis
            if crop_name.lower() == "rice":
                detected_issues = [
                    {
                        "type": "disease",
                        "name": "Rice Blast",
                        "confidence": 0.87,
                        "data": next((d for d in crop_issues["diseases"] if d["name"] == "Rice Blast"), None)
                    }
                ]
            elif crop_name.lower() == "wheat":
                detected_issues = [
                    {
                        "type": "disease",
                        "name": "Wheat Rust",
                        "confidence": 0.92,
                        "data": next((d for d in crop_issues["diseases"] if d["name"] == "Wheat Rust"), None)
                    }
                ]
            elif crop_name.lower() == "tomato":
                detected_issues = [
                    {
                        "type": "disease",
                        "name": "Early Blight",
                        "confidence": 0.78,
                        "data": next((d for d in crop_issues["diseases"] if d["name"] == "Early Blight"), None)
                    }
                ]
            elif crop_name.lower() == "cotton":
                detected_issues = [
                    {
                        "type": "pest",
                        "name": "Cotton Aphid",
                        "confidence": 0.83,
                        "data": next((p for p in crop_issues["pests"] if p["name"] == "Cotton Aphid"), None)
                    }
                ]
            else:
                # For other crops, simulate a "no issues detected" response
                detected_issues = []
                
            return {
                "success": True,
                "crop": crop_name,
                "detected_issues": detected_issues,
                "healthy": len(detected_issues) == 0
            }
            
        except Exception as e:
            logging.error(f"Error analyzing image: {str(e)}")
            return {
                "success": False,
                "error": f"Error analyzing image: {str(e)}"
            }
            
    def get_pesticide_recommendations(self, pest_or_disease_name, organic_preference=False):
        """
        Get pesticide recommendations for a specific pest or disease
        
        Args:
            pest_or_disease_name: Name of the pest or disease
            organic_preference: Whether to prioritize organic solutions
            
        Returns:
            Dictionary with pesticide recommendations
        """
        # Search for the pest or disease across all crops
        found_in_crops = []
        treatment_info = None
        
        for crop, data in self.pest_disease_db.items():
            # Search in pests
            for pest in data["pests"]:
                if pest["name"].lower() == pest_or_disease_name.lower():
                    found_in_crops.append(crop)
                    treatment_info = pest
                    issue_type = "pest"
                    break
                    
            # Search in diseases
            for disease in data["diseases"]:
                if disease["name"].lower() == pest_or_disease_name.lower():
                    found_in_crops.append(crop)
                    treatment_info = disease
                    issue_type = "disease"
                    break
        
        if not treatment_info:
            return {
                "success": False,
                "error": f"Pest or disease '{pest_or_disease_name}' not found in database"
            }
        
        # Define separate recommendations for organic and conventional approaches
        if issue_type == "pest":
            organic_options = [
                "Neem oil spray (5ml/L) applied weekly",
                "Garlic-chili spray (crush 100g each, soak overnight, dilute 1:10)",
                "Release beneficial insects like ladybugs or lacewings",
                "Diatomaceous earth dusted on plants",
                "Sticky yellow or blue traps for flying insects"
            ]
            
            conventional_options = [
                treatment_info["treatment"],
                "Consult local agricultural extension for region-specific chemical controls"
            ]
        else:  # disease
            organic_options = [
                "Copper-based fungicide (approved for organic use)",
                "Sulfur dust for powdery mildew issues",
                "Bacillus subtilis sprays for bacterial control",
                "Compost tea soil drench to improve plant immunity",
                "Milk spray (1:10 dilution) for fungal issues"
            ]
            
            conventional_options = [
                treatment_info["treatment"],
                "Consult local agricultural extension for region-specific fungicide options"
            ]
        
        # Return appropriate recommendations based on preference
        return {
            "success": True,
            "name": pest_or_disease_name,
            "type": issue_type,
            "affected_crops": found_in_crops,
            "treatment": treatment_info["treatment"],
            "prevention": treatment_info["prevention"],
            "recommendations": organic_options if organic_preference else conventional_options,
            "alternative_options": conventional_options if organic_preference else organic_options
        }
        
    def get_all_crops(self):
        """Get a list of all crops in the database"""
        return list(self.pest_disease_db.keys())


# Initialize the image pest detector
image_pest_detector = ImagePestDetector()