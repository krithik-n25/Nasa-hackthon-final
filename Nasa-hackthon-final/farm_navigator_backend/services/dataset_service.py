import json
from pathlib import Path

class DatasetService:
    def __init__(self):
        self.data_dir = Path("data")
        self.datasets_metadata = self._load_metadata()
    
    def _load_metadata(self):
        """Load dataset metadata from JSON file"""
        metadata_path = self.data_dir / "datasets_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        return self._get_default_metadata()
    
    def _get_default_metadata(self):
        """Return default dataset metadata"""
        return [
            {
                "id": "smap_soil_moisture",
                "name": "SMAP - Soil Moisture",
                "description": "Global soil moisture data from NASA's SMAP satellite",
                "source": "NASA SMAP",
                "variables": ["soil_moisture", "temperature"],
                "last_updated": "2025-09-30",
                "coverage_area": "Global",
                "temporal_resolution": "Daily",
                "spatial_resolution": "9km"
            },
            {
                "id": "gpm_precipitation",
                "name": "GPM - Precipitation",
                "description": "Real-time rainfall measurements worldwide",
                "source": "NASA GPM",
                "variables": ["precipitation", "rainfall_rate"],
                "last_updated": "2025-09-30",
                "coverage_area": "Global",
                "temporal_resolution": "Hourly",
                "spatial_resolution": "10km"
            },
            {
                "id": "modis_ndvi",
                "name": "MODIS NDVI - Vegetation Health",
                "description": "Vegetation health index from MODIS satellite",
                "source": "NASA MODIS",
                "variables": ["ndvi", "evi"],
                "last_updated": "2025-09-29",
                "coverage_area": "Global",
                "temporal_resolution": "16-day",
                "spatial_resolution": "250m"
            },
            {
                "id": "modis_lst",
                "name": "MODIS LST - Land Surface Temperature",
                "description": "Land surface temperature measurements",
                "source": "NASA MODIS",
                "variables": ["day_temperature", "night_temperature"],
                "last_updated": "2025-09-29",
                "coverage_area": "Global",
                "temporal_resolution": "Daily",
                "spatial_resolution": "1km"
            },
            {
                "id": "ecostress",
                "name": "ECOSTRESS - Evapotranspiration",
                "description": "Crop stress and water use efficiency data",
                "source": "NASA ECOSTRESS",
                "variables": ["evapotranspiration", "water_stress_index"],
                "last_updated": "2025-09-28",
                "coverage_area": "Global",
                "temporal_resolution": "Variable",
                "spatial_resolution": "70m"
            },
            {
                "id": "gldas",
                "name": "GLDAS - Soil Moisture & Energy Flux",
                "description": "Land surface model data including soil moisture",
                "source": "NASA GLDAS",
                "variables": ["soil_moisture_0-10cm", "soil_temperature"],
                "last_updated": "2025-09-30",
                "coverage_area": "Global",
                "temporal_resolution": "3-hourly",
                "spatial_resolution": "0.25 degree"
            },
            {
                "id": "modis_flood",
                "name": "MODIS Flood Maps",
                "description": "Near real-time flood detection and monitoring",
                "source": "NASA MODIS",
                "variables": ["flood_extent", "water_level"],
                "last_updated": "2025-09-30",
                "coverage_area": "Global",
                "temporal_resolution": "Daily",
                "spatial_resolution": "250m"
            },
            {
                "id": "landsat",
                "name": "Landsat - High-Resolution Imagery",
                "description": "High-resolution land and crop mapping",
                "source": "NASA/USGS Landsat",
                "variables": ["surface_reflectance", "land_cover"],
                "last_updated": "2025-09-25",
                "coverage_area": "Global",
                "temporal_resolution": "16-day",
                "spatial_resolution": "30m"
            },
            {
                "id": "grace",
                "name": "GRACE - Groundwater/Drought",
                "description": "Groundwater storage and drought monitoring",
                "source": "NASA GRACE-FO",
                "variables": ["groundwater_storage", "drought_index"],
                "last_updated": "2025-09-20",
                "coverage_area": "Global",
                "temporal_resolution": "Monthly",
                "spatial_resolution": "300km"
            },
            {
                "id": "crop_casma",
                "name": "Crop-CASMA - Crop Productivity",
                "description": "Crop productivity and soil condition analysis",
                "source": "NASA Crop-CASMA",
                "variables": ["crop_yield_anomaly", "soil_condition_index"],
                "last_updated": "2025-09-28",
                "coverage_area": "Agricultural regions",
                "temporal_resolution": "Weekly",
                "spatial_resolution": "1km"
            }
        ]
    
    def get_all_datasets(self):
        """Get simplified list of all datasets"""
        return [
            {
                "id": ds["id"],
                "name": ds["name"],
                "description": ds["description"]
            }
            for ds in self.datasets_metadata
        ]
    
    def get_dataset_by_id(self, dataset_id: str):
        """Get detailed dataset information"""
        for ds in self.datasets_metadata:
            if ds["id"] == dataset_id:
                return ds
        return None
