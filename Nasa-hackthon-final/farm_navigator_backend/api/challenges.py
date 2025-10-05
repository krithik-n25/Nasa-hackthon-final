# api/challenges.py
import json
from pathlib import Path
from typing import List
import asyncio

from fastapi import APIRouter, HTTPException
from ..models.schemas import Challenge
from ..services.nasa_power import get_live_weather_data

router = APIRouter()

# Define the path to the scenarios.json file
DATA_PATH = Path(__file__).parent.parent / "data" / "scenarios.json"

def load_challenges_from_db() -> List[dict]:
    """Loads raw challenge data from the JSON file."""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

@router.get("/", response_model=List[Challenge])
async def get_all_challenges_dynamically():
    """
    Endpoint to retrieve all challenges, dynamically updating their
    initial state with live data from the NASA POWER API.
    """
    static_challenges = load_challenges_from_db()
    if not static_challenges:
        raise HTTPException(status_code=404, detail="Challenges data not found.")

    # --- DYNAMIC DATA FETCHING ---
    # Create a list of tasks to fetch weather for all challenges concurrently
    tasks = []
    # Create a mapping to keep track of which task belongs to which challenge
    challenge_task_map = {}
    for i, challenge_data in enumerate(static_challenges):
        coords = challenge_data.get("coordinates")
        if coords:
            task = get_live_weather_data(coords["lat"], coords["lon"])
            tasks.append(task)
            challenge_task_map[i] = len(tasks) - 1 # Map challenge index to task index

    # Run all the API calls at the same time and handle potential errors
    live_weather_results = await asyncio.gather(*tasks, return_exceptions=True)

    # --- MERGE STATIC AND DYNAMIC DATA ---
    dynamic_challenges = []
    for i, challenge_data in enumerate(static_challenges):
        # If this challenge had a task associated with it, update its data
        if i in challenge_task_map:
            task_index = challenge_task_map[i]
            result = live_weather_results[task_index]
            
            # Check if the API call was successful and returned a dictionary
            if isinstance(result, dict):
                challenge_data["initial_state"]["temperature"] = result["temperature"]
            else:
                # If the API call failed, log the error but proceed with static data
                print(f"API call failed for challenge {challenge_data['id']}: {result}")
        
        # Validate the final, merged data with Pydantic and add to our list
        dynamic_challenges.append(Challenge(**challenge_data))

    return dynamic_challenges



# ============================================================
# 🔧 NEW ENDPOINT - Get individual challenge by ID
# ============================================================

@router.get("/{challenge_id}", response_model=Challenge)
async def get_challenge_by_id(challenge_id: int):
    """
    Endpoint to retrieve a specific challenge by its ID,
    with live weather data from NASA POWER API.
    """
    static_challenges = load_challenges_from_db()
    
    if not static_challenges:
        raise HTTPException(status_code=404, detail="Challenges data not found.")
    
    # Find the challenge with matching ID
    challenge_data = next(
        (c for c in static_challenges if c.get("id") == challenge_id), 
        None
    )
    
    if not challenge_data:
        raise HTTPException(
            status_code=404, 
            detail=f"Challenge with ID {challenge_id} not found."
        )
    
    # Fetch live weather data if coordinates exist
    coords = challenge_data.get("coordinates")
    if coords and "lat" in coords and "lon" in coords:
        try:
            live_data = await get_live_weather_data(coords["lat"], coords["lon"])
            if isinstance(live_data, dict) and "temperature" in live_data:
                challenge_data["initial_state"]["temperature"] = live_data["temperature"]
        except Exception as e:
            # If live data fails, continue with static data
            print(f"Warning: Could not fetch live data: {e}")
    
    return Challenge(**challenge_data)
