from fastapi import APIRouter, HTTPException
from farm_navigator_backend.services.dataset_service import DatasetService
from farm_navigator_backend.models.schemas1 import DatasetResponse, DatasetDetailResponse

router = APIRouter()
dataset_service = DatasetService()

@router.get("/", response_model=list[DatasetResponse])
async def get_all_datasets():
    """Get list of all available datasets"""
    try:
        datasets = dataset_service.get_all_datasets()
        return datasets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_id}", response_model=DatasetDetailResponse)
async def get_dataset_detail(dataset_id: str):
    """Get detailed information about a specific dataset"""
    try:
        dataset = dataset_service.get_dataset_by_id(dataset_id)
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
        return dataset
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))