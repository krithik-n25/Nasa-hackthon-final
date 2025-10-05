from fastapi import APIRouter, HTTPException
from farm_navigator_backend.services.graph_service import GraphService
from farm_navigator_backend.models.schemas1 import GraphDataResponse, GraphFilterRequest

router = APIRouter()
graph_service = GraphService()

@router.get("/{dataset_id}", response_model=GraphDataResponse)
async def get_graph_data(dataset_id: str):
    """Get graph data for a specific dataset"""
    try:
        graph_data = graph_service.get_graph_data(dataset_id)
        if not graph_data:
            raise HTTPException(status_code=404, detail="Graph data not found")
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/filter")
async def get_filtered_graph_data(filter_request: GraphFilterRequest):
    """Get filtered graph data based on date range and location"""
    try:
        graph_data = graph_service.get_filtered_graph_data(
            filter_request.dataset_id,
            filter_request.start_date,
            filter_request.end_date,
            filter_request.location
        )
        return graph_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))