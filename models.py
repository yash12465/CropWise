from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class CropConditions:
    """Class for storing optimal crop growing conditions"""
    n_min: float
    n_max: float
    p_min: float
    p_max: float
    k_min: float
    k_max: float
    temperature_min: float
    temperature_max: float
    humidity_min: float
    humidity_max: float
    ph_min: float
    ph_max: float
    rainfall_min: float
    rainfall_max: float
    description: str
