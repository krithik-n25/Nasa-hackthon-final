# nasa_api_app/models/nasa_schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# --- 1. Schemas for Current Conditions API (/api/nasa-data) ---

class CurrentConditionsRequest(BaseModel):
    """Inputs for fetching current NASA data (via GET query parameters)."""
    lat: float
    lon: float
    type: str

class CurrentConditionsResponse(BaseModel):
    """Response structure for fetched current conditions."""
    # The frontend specifically looks for 'soil_moisture' (integer)
    soil_moisture: Optional[int] = Field(None, description="Current soil moisture level (e.g., 0-100).")


# --- 2. Schemas for Schedule Generation API (/api/generate-schedule) ---

class ScheduleInput(BaseModel):
    """Inputs from the frontend farm form (POST request body)."""
    crop_type: str
    farm_size: float
    latitude: float
    longitude: float
    soil_type: str
    # Validate soil moisture is between 0 and 100, as it's a key input
    soil_moisture: int = Field(..., ge=0, le=100)
    soil_temperature: Optional[float] = None
    soil_fertility: str
    sunlight: int = Field(..., ge=0, le=100)
    rainfall: Optional[float] = None
    # This matches the frontend's logic of splitting "min-max" into a list [min, max]
    temperature_range: Optional[List[int]] = None 
    wind_speed: Optional[float] = None
    water_availability: str
    labor_availability: str
    machinery_access: bool
    budget: str
    objective: str
    season: str


# --- 3. Schema for the Final Action Schedule (Output) ---

class ActionItem(BaseModel):
    """Structure for a single action/task returned to the frontend."""
    icon: str
    title: str
    date: str
    field_area: str
    details: str
    type: str # e.g., 'Water Management', 'Extreme Heat Mitigation'
    reason: Optional[str] = None
    