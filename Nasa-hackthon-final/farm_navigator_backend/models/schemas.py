# models/schemas.py
from pydantic import BaseModel
from typing import List, Literal, Optional, Dict

# --- Data Structures for Farm State ---
class FarmState(BaseModel):
    """Represents the current state of the farm in the simulation."""
    soil_moisture: float
    crop_health: float
    livestock_health: float
    budget: float
    yield_estimate: float = 0
    day: int = 1

class InitialState(BaseModel):
    temperature: int
    soil_moisture: int
    crop_health: int
    livestock_health: int
    budget: int
    
# --- Data Structures for Actions ---
ActionType = Literal["irrigate", "fertilize", "pesticide", "feed_livestock", "next_day"]

class Action(BaseModel):
    """Represents an action taken by the player."""
    action_type: ActionType

class SimulationRequest(BaseModel):
    """The request body for a simulation tick."""
    challenge_id: int
    current_state: FarmState
    action: Action

# --- Data Structures for API Responses ---
class SimulationResponse(BaseModel):
    """The response after a simulation tick."""
    new_state: FarmState
    message: str
    is_complete: bool = False
    is_success: Optional[bool] = None
    
# --- Data Structures for Challenges (from scenarios.json) ---
class Goal(BaseModel):
    description: str

# NEW: A model to validate the coordinates object
class Coordinates(BaseModel):
    lat: float
    lon: float
    
class Challenge(BaseModel):
    id: int
    title: str
    location: str
    description: str
    difficulty: str
    initial_state: InitialState
    goal: Goal
    datasets: List[str]
