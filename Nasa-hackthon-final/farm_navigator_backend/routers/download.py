from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from farm_navigator_backend.services.download_service import DownloadService
from farm_navigator_backend.models.schemas1 import CustomDownloadRequest

router = APIRouter()
download_service = DownloadService()

@router.get("/{dataset_id}")
async def download_dataset(
    dataset_id: str,
    format: str = Query("csv", regex="^(csv|json)$")
):
    """Download dataset in specified format"""
    try:
        file_content, filename = download_service.prepare_download(dataset_id, format)
        
        media_type = "text/csv" if format == "csv" else "application/json"
        
        return StreamingResponse(
            iter([file_content]),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/custom")
async def download_custom_dataset(request: CustomDownloadRequest):
    """Download customized dataset with filters"""
    try:
        file_content, filename = download_service.prepare_custom_download(
            request.dataset_id,
            request.format,
            request.start_date,
            request.end_date,
            request.variables
        )
        
        media_type = "text/csv" if request.format == "csv" else "application/json"
        
        return StreamingResponse(
            iter([file_content]),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))