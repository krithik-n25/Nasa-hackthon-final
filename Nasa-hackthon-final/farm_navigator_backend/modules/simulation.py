# modules/simulation.py
# This file contains the logic for the "What if?" simulator, starting with
# a simple yield prediction model.

import random

# Base yield values (in tons/hectare) for different crops.
# These are simplified averages.
BASE_YIELDS = {
    "maize": 4.5,
    "wheat": 3.2,
    "rice": 5.0,
    "soybean": 2.8,
    "default": 3.5
}

def predict_yield(crop_type: str, health_score: int) -> float:
    """
    A simple simulation engine to predict crop yield.
    
    In a more advanced version, this model would also take into account:
    - Soil moisture and nutrient levels
    - Historical and forecasted weather
    - Player actions (irrigation, fertilization)
    
    Args:
        crop_type (str): The type of crop (e.g., 'maize').
        health_score (int): The current health of the crop (0-100).
        
    Returns:
        float: The predicted yield in tons per hectare.
    """
    base = BASE_YIELDS.get(crop_type.lower(), BASE_YIELDS["default"])
    
    # The health score acts as a multiplier on the base yield.
    # A score of 80 means 80% of the potential yield is expected.
    # We add a small random factor to make it feel more dynamic.
    health_modifier = (health_score / 100) * random.uniform(0.98, 1.02)
    
    predicted = base * health_modifier
    
    return round(predicted, 2)
