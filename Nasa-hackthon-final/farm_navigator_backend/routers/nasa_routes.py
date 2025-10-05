# nasa_api_app/routers/nasa_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from ..services.nasa_fetcher import NASAFetcher
from ..models.nasa_schemas import (
    CurrentConditionsResponse, 
    ScheduleInput, 
    ActionItem,
    CurrentConditionsRequest
)

# Initialize the router and the service layer
router = APIRouter()
nasa_fetcher = NASAFetcher()

# ----------------------------------------------------------------------
# 1. Endpoint for fetching current NASA data (GET /api/nasa-data)
# ----------------------------------------------------------------------

@router.get(
    "/nasa-data", 
    response_model=CurrentConditionsResponse,
    summary="Fetch current NASA Earth Observation data for a location"
)
async def get_nasa_data(
    # FastAPI automatically extracts these from the URL query parameters
    lat: float = Query(..., description="Latitude of the farm area."),
    lon: float = Query(..., description="Longitude of the farm area."),
    type: str = Query(..., description="Type of data requested (e.g., 'moisture').")
):
    """
    Called by the frontend's 'Auto Fetch' button to populate form fields 
    using real-time NASA data.
    """
    
    request_data = CurrentConditionsRequest(lat=lat, lon=lon, type=type)

    try:
        # Calls the NASAFetcher (Step 3) to get the data
        data = nasa_fetcher.fetch_current_conditions(
            lat=request_data.lat, 
            lon=request_data.lon, 
            data_type=request_data.type
        )
        return data
    except Exception as e:
        # Return a server error if the service call failed
        raise HTTPException(status_code=500, detail=f"Failed to fetch NASA data: {str(e)}")


# ----------------------------------------------------------------------
# 2. Endpoint for generating the final schedule (POST /api/generate-schedule)
# ----------------------------------------------------------------------

@router.post(
    "/generate-schedule",
    response_model=List[ActionItem],
    summary="Generate a farm action schedule based on farm data and NASA Pathfinders"
)
async def generate_schedule(input_data: ScheduleInput):
    """
    Receives the full farm data (POST body) and generates a list of recommended actions/tasks.
    """
    
    print(f"Schedule Generator: Analyzing inputs for crop: {input_data.crop_type}")

    # --- CORE LOGIC: Apply NASA Pathfinder Analysis ---
    
    actions: List[ActionItem] = []
    
    # Example 1: Logic based on the Drought Pathfinder (Agriculture and Water Management)
    if input_data.soil_moisture < 35:
        actions.append(ActionItem(
            icon="💧",
            title="Critical Irrigation Alert",
            date="2025-10-06", # Placeholder date
            field_area="All Areas",
            details=f"Soil moisture ({input_data.soil_moisture}%) is critically low. Immediate deep watering is required to save the {input_data.crop_type} crop.",
            type="Water Management",
            reason="Drought Pathfinder: SMAP data analysis indicates severe dry conditions."
        ))

    # Example 2: Logic based on the Extreme Heat Data Pathfinder
    if input_data.temperature_range and max(input_data.temperature_range) > 40:
        actions.append(ActionItem(
            icon="🔥",
            title="Extreme Heat Crop Protection",
            date="2025-10-08",
            field_area="Western Field",
            details="NASA Land Surface Temperature analysis predicts high stress. Apply anti-transpirants or shade nets.",
            type="Extreme Heat Mitigation",
            reason="Extreme Heat Pathfinder: High temperature risk predicted."
        ))

    # Example 3: General Harvest Portal/Acres Recommendation
    actions.append(ActionItem(
        icon="📅",
        title="Mid-Season Crop Health Assessment",
        date="2025-10-15",
        field_area="Field 1",
        details="Perform a detailed field survey for pest/disease detection based on NASA Harvest guidelines.",
        type="General Maintenance",
        reason="NASA Harvest Consortium recommendation for crop type."
    ))

    return actions