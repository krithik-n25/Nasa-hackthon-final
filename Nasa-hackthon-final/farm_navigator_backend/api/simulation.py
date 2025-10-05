# api/simulation.py
from fastapi import APIRouter
from ..models.schemas import SimulationRequest, SimulationResponse

router = APIRouter()

# Constants for game logic - easy to tweak
IRRIGATION_COST = 100
FERTILIZER_COST = 150
PESTICIDE_COST = 80
LIVESTOCK_FEED_COST = 50

DAILY_MOISTURE_LOSS = 5.0
DAILY_HEALTH_LOSS_DRY = 8.0
DAILY_HEALTH_GAIN_WET = 4.0

@router.post("/action", response_model=SimulationResponse)
async def process_simulation_action(request: SimulationRequest):
    """
    Processes a single player action and updates the farm state.
    This is the core game logic engine.
    """
    state = request.current_state
    action = request.action
    message = ""

    # --- 1. Process Player Actions ---
    if action.action_type == "irrigate":
        if state.budget >= IRRIGATION_COST:
            state.budget -= IRRIGATION_COST
            state.soil_moisture = min(100.0, state.soil_moisture + 30.0)
            message = "Irrigation successful. Soil moisture increased."
        else:
            message = "Not enough budget for irrigation."

    elif action.action_type == "fertilize":
        if state.budget >= FERTILIZER_COST:
            state.budget -= FERTILIZER_COST
            state.crop_health = min(100.0, state.crop_health + 25.0)
            message = "Fertilizer applied. Crop health boosted."
        else:
            message = "Not enough budget for fertilizer."

    elif action.action_type == "pesticide":
        if state.budget >= PESTICIDE_COST:
            state.budget -= PESTICIDE_COST
            # In a more complex sim, this would prevent a negative event
            message = "Pesticides applied, crops are protected."
        else:
            message = "Not enough budget for pesticides."
            
    elif action.action_type == "feed_livestock":
        if state.budget >= LIVESTOCK_FEED_COST:
            state.budget -= LIVESTOCK_FEED_COST
            state.livestock_health = min(100.0, state.livestock_health + 20.0)
            message = "Livestock have been fed."
        else:
            message = "Not enough budget to feed livestock."

    elif action.action_type == "next_day":
        # --- 2. Simulate Natural Processes for the Day ---
        state.day += 1
        
        # Soil moisture decreases naturally (evaporation)
        state.soil_moisture = max(0.0, state.soil_moisture - DAILY_MOISTURE_LOSS)

        # Crop health changes based on soil moisture
        if state.soil_moisture < 30:
            state.crop_health = max(0.0, state.crop_health - DAILY_HEALTH_LOSS_DRY)
            message = "A new day has begun. Warning: soil is too dry! Crops are suffering."
        elif state.soil_moisture > 60:
            state.crop_health = min(100.0, state.crop_health + DAILY_HEALTH_GAIN_WET)
            message = "A new day has begun. The crops are thriving with sufficient water."
        else:
            message = "A new day has begun. Conditions are stable."
        
        # Livestock health decreases slightly each day
        state.livestock_health = max(0.0, state.livestock_health - 3.0)


    # --- 3. Update derived values ---
    # Yield is a function of crop health
    state.yield_estimate = round(state.crop_health * 5.5, 2)

    # --- 4. Check for Win/Loss Conditions ---
    is_complete = False
    is_success = None
    
    # Example win/loss condition
    if state.day > 7: 
        is_complete = True
        
        if state.yield_estimate >= 400 and state.crop_health >= 60:
            is_success = True
            message = f"🎉 Mission Success! Final yield: {state.yield_estimate}kg with {state.crop_health}% crop health"
        elif state.yield_estimate >= 200:
            is_success = False
            message = f"❌ Mission Failed. Yield too low: {state.yield_estimate}kg (needed 300kg+)"
        else:
            is_success = False
            message = f"❌ Mission Failed. Critical crop failure: {state.yield_estimate}kg yield"

    return SimulationResponse(
        new_state=state,
        message=message,
        is_complete=is_complete,
        is_success=is_success
    )
