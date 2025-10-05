# nasa_api_app/services/nasa_fetcher.py
import requests
from ..core.config import settings
from ..models.nasa_schemas import CurrentConditionsResponse
import random # We keep random for the soil moisture MOCK for now

class NASAFetcher:
    """Handles fetching real, non-static data from NASA APIs."""

    def __init__(self):
        self.api_key = settings.NASA_API_KEY
        self.base_url = "https://eonet.gsfc.nasa.gov/api/v3/" # EONET V3 BASE URL

    def _fetch_eonet_events(self, lat: float, lon: float, category_id: str) -> bool:
        """Helper to check EONET for open events in a bounding box."""
        
        # Define a small bounding box (bbox) around the farm (e.g., 1 degree = approx 111km)
        # Bbox format for EONET v3: min lon, min lat, max lon, max lat
        bbox_size = 0.5 # +/- 0.5 degree (roughly 55km radius)
        bbox = f"{lon - bbox_size},{lat - bbox_size},{lon + bbox_size},{lat + bbox_size}"

        params = {
            'api_key': self.api_key, # Your TEST_KEY_123 or real key
            'category': category_id,
            'status': 'open',
            'limit': 1, # Only need one to confirm an event is happening
            'days': 7, # Check for events in the last 7 days
            'bbox': bbox 
        }

        try:
            response = requests.get(f"{self.base_url}events", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Returns True if any open events are found within the bounding box
            return bool(data.get('events')) 
        
        except requests.RequestException as e:
            print(f"EONET API Error: {e}")
            return False # Assume no event on failure


    def fetch_current_conditions(self, lat: float, lon: float, data_type: str) -> CurrentConditionsResponse:
        """
        Fetches current conditions (like soil moisture) near the given lat/lon.
        
        NOTE: Soil moisture remains a MOCK, but its value is now influenced by the EONET API call.
        """
        
        print(f"FETCH: Requesting '{data_type}' data for Lat:{lat}, Lon:{lon} using EONET and MOCK.")
        
        if data_type == 'moisture':
            
            # --- EONET INTEGRATION: Check for Drought events (Category ID 6) ---
            is_drought_event_nearby = self._fetch_eonet_events(lat, lon, 'drought') # 'drought' is the v3 category title
            
            # --- MOCK LOGIC START ---
            # Generate a baseline mock value (40-65)
            moisture_value = int((lat * 1.5 + lon * 0.8) % 25) + 40
            
            if is_drought_event_nearby:
                # If EONET confirms a drought event, force the soil moisture low (below the critical threshold of 35)
                moisture_value = random.randint(15, 30) 
            
            moisture_value = min(max(moisture_value, 10), 85) # Clamp range
            
            print(f"Soil Moisture Result: {moisture_value}%. Drought event nearby: {is_drought_event_nearby}")
            
            return CurrentConditionsResponse(soil_moisture=moisture_value)
            # --- MOCK LOGIC END ---

        # Return empty response for unhandled types
        return CurrentConditionsResponse()