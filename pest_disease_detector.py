import os
import json
import logging
from datetime import datetime

class PestDiseaseDetector:
    """A class for identifying crop pests and diseases and providing treatment recommendations"""
    
    def __init__(self):
        self.pest_disease_data = self._load_pest_disease_database()
    
    def _load_pest_disease_database(self):
        """Load pest and disease database from JSON file"""
        try:
            # Check if database file exists
            if os.path.exists('pest_disease_database.json'):
                with open('pest_disease_database.json', 'r') as f:
                    return json.load(f)
            
            # If file doesn't exist, create a default database
            data = self._create_default_database()
            
            # Save the default database
            with open('pest_disease_database.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            return data
        except Exception as e:
            logging.error(f"Error loading pest and disease database: {str(e)}")
            return self._create_default_database()
    
    def _create_default_database(self):
        """Create a default pest and disease database"""
        return {
            "rice": {
                "pests": [
                    {
                        "name": "Brown Planthopper",
                        "symptoms": ["Yellowing of leaves", "Wilting", "Hopper burn", "Stunted growth"],
                        "image": "brown_planthopper.jpg",
                        "description": "Small brown insects that suck sap from the rice plant's base, causing the plants to wilt and eventually die.",
                        "treatment": "Use resistant rice varieties, maintain clean fields, apply appropriate insecticides when thresholds are reached, encourage natural enemies like spiders and beetles.",
                        "prevention": "Plant resistant varieties, avoid excessive nitrogen application, maintain clean fields and remove weeds."
                    },
                    {
                        "name": "Rice Stem Borer",
                        "symptoms": ["Dead central leaf (deadheart)", "White empty panicles (whitehead)", "Holes in stems"],
                        "image": "rice_stem_borer.jpg",
                        "description": "Caterpillars that bore into rice stems, causing the central leaf to die or panicles to become empty.",
                        "treatment": "Apply appropriate insecticides at the right timing, use light traps to catch adult moths.",
                        "prevention": "Plant resistant varieties, synchronize planting with neighboring fields, plow fields after harvest to kill remaining larvae."
                    }
                ],
                "diseases": [
                    {
                        "name": "Rice Blast",
                        "symptoms": ["Diamond-shaped lesions on leaves", "Infected neck turning brown", "Empty grains"],
                        "image": "rice_blast.jpg",
                        "description": "Fungal disease causing lesions on leaves, necks, and panicles, leading to significant yield loss.",
                        "treatment": "Apply fungicides at the right timing, particularly at the early heading stage.",
                        "prevention": "Plant resistant varieties, avoid excessive nitrogen fertilization, maintain proper water management."
                    },
                    {
                        "name": "Bacterial Leaf Blight",
                        "symptoms": ["Water-soaked lesions on leaf edges", "Lesions turning yellow to white", "Wilted leaves"],
                        "image": "bacterial_leaf_blight.jpg",
                        "description": "Bacterial disease causing water-soaked lesions that turn yellow to white, eventually killing the leaves.",
                        "treatment": "No effective chemical control once infection occurs. Remove infected plants and maintain field sanitation.",
                        "prevention": "Plant resistant varieties, avoid wounds on plants, use balanced fertilization, practice crop rotation."
                    }
                ]
            },
            "maize": {
                "pests": [
                    {
                        "name": "Fall Armyworm",
                        "symptoms": ["Skeletonized leaves", "Holes in leaves and stems", "Frass (insect excrement) in whorls"],
                        "image": "fall_armyworm.jpg",
                        "description": "Caterpillars that feed on leaves and stems, causing significant damage to maize plants.",
                        "treatment": "Apply appropriate insecticides when infestation levels reach threshold, use biological controls like Bacillus thuringiensis (Bt).",
                        "prevention": "Plant early, use trap crops, encourage natural enemies, plant Bt maize varieties where available."
                    },
                    {
                        "name": "Maize Weevil",
                        "symptoms": ["Holes in stored grain", "Grain dust", "Adult weevils in storage"],
                        "image": "maize_weevil.jpg", 
                        "description": "Small beetles that infest stored maize, causing weight loss and quality deterioration.",
                        "treatment": "Fumigation of storage areas, use of appropriate storage insecticides.",
                        "prevention": "Ensure grain is properly dried before storage, use clean storage facilities, use hermetic storage bags."
                    }
                ],
                "diseases": [
                    {
                        "name": "Northern Leaf Blight",
                        "symptoms": ["Long, elliptical gray-green lesions", "Lesions turn tan-brown", "Lower leaves affected first"],
                        "image": "northern_leaf_blight.jpg",
                        "description": "Fungal disease causing long lesions on leaves, reducing photosynthetic area and yield.",
                        "treatment": "Apply fungicides when disease appears, especially in humid conditions.",
                        "prevention": "Plant resistant varieties, practice crop rotation, plow under crop residue after harvest."
                    },
                    {
                        "name": "Maize Lethal Necrosis",
                        "symptoms": ["Yellowing and mottling of leaves", "Dead leaf margins", "Stunted growth", "Poor or no seed set"],
                        "image": "maize_lethal_necrosis.jpg",
                        "description": "Viral disease complex causing severe symptoms and yield loss.",
                        "treatment": "No cure once infected. Remove and destroy infected plants.",
                        "prevention": "Plant resistant varieties, control insect vectors like aphids, practice crop rotation, use certified seeds."
                    }
                ]
            },
            "beans": {
                "pests": [
                    {
                        "name": "Bean Aphid",
                        "symptoms": ["Clusters of small black/green insects", "Curled leaves", "Sticky honeydew on leaves", "Sooty mold growth"],
                        "image": "bean_aphid.jpg",
                        "description": "Small sap-sucking insects that feed on plant juices, causing leaves to curl and stunting growth.",
                        "treatment": "Apply insecticidal soap or neem oil, introduce ladybugs or lacewings as natural predators.",
                        "prevention": "Use reflective mulches to repel aphids, maintain proper plant spacing for good air circulation."
                    },
                    {
                        "name": "Bean Weevil",
                        "symptoms": ["Small holes in dried beans", "Adult beetles emerging from stored beans", "Reduced seed germination"],
                        "image": "bean_weevil.jpg",
                        "description": "Beetles that lay eggs on developing bean pods, with larvae feeding inside the beans.",
                        "treatment": "Freezing infested beans for 4 days, heating beans to 60°C for 45 minutes, or using diatomaceous earth in storage.",
                        "prevention": "Harvest promptly, discard infested seeds, use airtight containers for storage, use resistant varieties."
                    }
                ],
                "diseases": [
                    {
                        "name": "Bean Rust",
                        "symptoms": ["Small yellow spots on leaf undersides", "Rusty-brown pustules", "Premature leaf drop"],
                        "image": "bean_rust.jpg",
                        "description": "Fungal disease causing rusty pustules primarily on leaf undersides, reducing photosynthesis and yield.",
                        "treatment": "Apply appropriate fungicides when symptoms first appear, remove heavily infected plants.",
                        "prevention": "Plant resistant varieties, avoid overhead irrigation, maintain proper plant spacing, practice crop rotation."
                    },
                    {
                        "name": "Bean Common Mosaic Virus",
                        "symptoms": ["Mottled light/dark green pattern on leaves", "Leaf curling", "Stunted growth", "Reduced yield"],
                        "image": "bean_common_mosaic.jpg",
                        "description": "Viral disease causing mosaic patterns on leaves and reduced plant vigor and yield.",
                        "treatment": "No cure once infected. Remove and destroy infected plants to prevent spread.",
                        "prevention": "Use certified disease-free seeds, control aphid vectors, clean tools between plants, plant resistant varieties."
                    }
                ]
            },
            "tomato": {
                "pests": [
                    {
                        "name": "Tomato Hornworm",
                        "symptoms": ["Large sections of leaves eaten", "Stems eaten", "Black frass (excrement)", "Large green caterpillars"],
                        "image": "tomato_hornworm.jpg",
                        "description": "Large green caterpillars with a horn-like projection that can rapidly defoliate tomato plants.",
                        "treatment": "Handpick and remove caterpillars, apply Bacillus thuringiensis (Bt), introduce parasitic wasps.",
                        "prevention": "Till soil after harvest to destroy pupae, attract natural predators with companion planting."
                    },
                    {
                        "name": "Whitefly",
                        "symptoms": ["Small white flying insects under leaves", "Yellowing leaves", "Sticky honeydew", "Sooty mold"],
                        "image": "whitefly.jpg",
                        "description": "Tiny white flying insects that suck plant sap and secrete honeydew, which can lead to sooty mold.",
                        "treatment": "Use yellow sticky traps, apply insecticidal soap or neem oil, introduce predatory insects.",
                        "prevention": "Use reflective mulches, apply row covers, maintain plant vigor with proper fertilization and watering."
                    }
                ],
                "diseases": [
                    {
                        "name": "Early Blight",
                        "symptoms": ["Dark brown spots with concentric rings", "Yellow area around spots", "Lower leaves affected first"],
                        "image": "early_blight.jpg",
                        "description": "Fungal disease causing dark spots with concentric rings, primarily on older leaves first.",
                        "treatment": "Apply fungicides preventatively or at first sign of disease, remove infected leaves.",
                        "prevention": "Mulch around plants, avoid overhead watering, ensure good air circulation, practice crop rotation."
                    },
                    {
                        "name": "Tomato Yellow Leaf Curl Virus",
                        "symptoms": ["Upward curling leaves", "Yellowing leaf edges", "Stunted growth", "Flower drop", "Reduced yield"],
                        "image": "tomato_yellow_leaf_curl.jpg",
                        "description": "Viral disease transmitted by whiteflies, causing leaf curling, yellowing and significant yield reduction.",
                        "treatment": "No cure once infected. Remove and destroy infected plants, control whitefly populations.",
                        "prevention": "Use resistant varieties, use reflective mulches to repel whiteflies, use row covers, control weeds."
                    }
                ]
            },
            "apple": {
                "pests": [
                    {
                        "name": "Codling Moth",
                        "symptoms": ["Tunnels in fruit with brown frass", "Exit holes in fruit", "Premature fruit drop"],
                        "image": "codling_moth.jpg",
                        "description": "Moths whose larvae tunnel into apples, causing significant fruit damage and drop.",
                        "treatment": "Apply targeted insecticides based on moth lifecycle, use pheromone traps or mating disruption.",
                        "prevention": "Remove fallen fruit promptly, use tree bands to trap larvae, thin fruit clusters to reduce hiding places."
                    },
                    {
                        "name": "Apple Maggot",
                        "symptoms": ["Dimpled or pitted fruit surface", "Winding brown tunnels in fruit flesh", "Fruit decay"],
                        "image": "apple_maggot.jpg",
                        "description": "Flies whose larvae tunnel throughout apple flesh, causing fruit to decay and drop prematurely.",
                        "treatment": "Hang red sphere traps with sticky coating, apply appropriate insecticides at key times.",
                        "prevention": "Pick up and destroy fallen fruit, use sticky traps to catch adults, use kaolin clay as a repellent."
                    }
                ],
                "diseases": [
                    {
                        "name": "Apple Scab",
                        "symptoms": ["Olive-green to brown spots on leaves", "Dark scabby lesions on fruit", "Premature leaf drop"],
                        "image": "apple_scab.jpg",
                        "description": "Fungal disease causing scab-like lesions on leaves and fruit, reducing marketability and tree vigor.",
                        "treatment": "Apply fungicides preventatively in spring before infection occurs, continue through wet periods.",
                        "prevention": "Plant resistant varieties, improve air circulation through pruning, rake and destroy fallen leaves."
                    },
                    {
                        "name": "Fire Blight",
                        "symptoms": ["Blackened twigs and branches", "Shepherd's crook on branch tips", "Bacterial ooze", "Fruit mummification"],
                        "image": "fire_blight.jpg",
                        "description": "Bacterial disease causing branch die-back and fruit decay, can be fatal to young trees.",
                        "treatment": "Prune out infected branches 12 inches below visible infection, apply copper-based bactericides.",
                        "prevention": "Plant resistant varieties, avoid excessive nitrogen fertilization, prune during dry weather."
                    }
                ]
            }
        }
    
    def get_common_pests_diseases(self, crop_name):
        """Get a list of common pests and diseases for a specific crop"""
        crop_name = crop_name.lower()
        
        if crop_name in self.pest_disease_data:
            return {
                "success": True,
                "crop": crop_name,
                "pests": self.pest_disease_data[crop_name]["pests"],
                "diseases": self.pest_disease_data[crop_name]["diseases"]
            }
        else:
            return {
                "success": False,
                "error": f"No pest and disease data available for {crop_name}"
            }
    
    def identify_issue(self, crop_name, symptoms):
        """Identify potential pest or disease issues based on symptoms"""
        crop_name = crop_name.lower()
        if crop_name not in self.pest_disease_data:
            return {
                "success": False,
                "error": f"No pest and disease data available for {crop_name}"
            }
            
        matches = []
        
        # Convert symptoms to lowercase for case-insensitive matching
        symptoms_lower = [symptom.lower() for symptom in symptoms]
        
        # Check for matching symptoms in pests
        for pest in self.pest_disease_data[crop_name]["pests"]:
            pest_symptoms_lower = [symptom.lower() for symptom in pest["symptoms"]]
            matching_symptoms = set(symptoms_lower) & set(pest_symptoms_lower)
            
            if matching_symptoms:
                match_percentage = (len(matching_symptoms) / len(pest_symptoms_lower)) * 100
                matches.append({
                    "type": "pest",
                    "name": pest["name"],
                    "match_percentage": match_percentage,
                    "matching_symptoms": list(matching_symptoms),
                    "data": pest
                })
        
        # Check for matching symptoms in diseases
        for disease in self.pest_disease_data[crop_name]["diseases"]:
            disease_symptoms_lower = [symptom.lower() for symptom in disease["symptoms"]]
            matching_symptoms = set(symptoms_lower) & set(disease_symptoms_lower)
            
            if matching_symptoms:
                match_percentage = (len(matching_symptoms) / len(disease_symptoms_lower)) * 100
                matches.append({
                    "type": "disease",
                    "name": disease["name"],
                    "match_percentage": match_percentage,
                    "matching_symptoms": list(matching_symptoms),
                    "data": disease
                })
        
        # Sort matches by match percentage (descending)
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        return {
            "success": True,
            "crop": crop_name,
            "matches": matches,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_all_crops(self):
        """Get a list of all crops in the database"""
        return list(self.pest_disease_data.keys())
    
    def add_pest_disease_data(self, crop_name, pest_or_disease_data, data_type):
        """Add new pest or disease data for a crop"""
        crop_name = crop_name.lower()
        
        # Create crop entry if it doesn't exist
        if crop_name not in self.pest_disease_data:
            self.pest_disease_data[crop_name] = {
                "pests": [],
                "diseases": []
            }
        
        # Add data to appropriate list
        if data_type.lower() == "pest":
            self.pest_disease_data[crop_name]["pests"].append(pest_or_disease_data)
        elif data_type.lower() == "disease":
            self.pest_disease_data[crop_name]["diseases"].append(pest_or_disease_data)
        else:
            return False
        
        # Save updated database
        try:
            with open('pest_disease_database.json', 'w') as f:
                json.dump(self.pest_disease_data, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error saving pest and disease database: {str(e)}")
            return False

# Initialize the pest and disease detector when the module is imported
pest_disease_detector = PestDiseaseDetector()