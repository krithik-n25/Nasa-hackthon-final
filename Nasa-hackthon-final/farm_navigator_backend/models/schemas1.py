from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DatasetResponse(BaseModel):
    id: str
    name: str
    description: str
    source: Optional[str] = None
    variables: Optional[List[str]] = None

class DatasetDetailResponse(DatasetResponse):
    last_updated: Optional[str] = None
    coverage_area: Optional[str] = None
    temporal_resolution: Optional[str] = None
    spatial_resolution: Optional[str] = None

class GraphDataResponse(BaseModel):
    dataset_id: str
    chart_type: str
    labels: List[str]
    datasets: List[dict]

class GraphFilterRequest(BaseModel):
    dataset_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None

class CustomDownloadRequest(BaseModel):
    dataset_id: str
    format: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    variables: Optional[List[str]] = None