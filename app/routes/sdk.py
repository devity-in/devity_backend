import uuid
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Import service function and db dependency
from app.services import spec_service
from app.database.database import get_db

# Create the router
router = APIRouter()

@router.get("/specs/{spec_id}", response_model=Dict[str, Any])
def get_spec_content_for_sdk(
    *, 
    session: Session = Depends(get_db), 
    spec_id: uuid.UUID,
    # TODO: Add API Key authentication dependency here later
) -> Dict[str, Any]:
    """Get the raw content of the latest draft spec for the SDK (Debug Mode).
    
    Note: This endpoint bypasses versioning and publishing for development.
    Requires API Key authentication in the future.
    """
    # Use get_spec_or_404 to ensure the spec exists
    spec = spec_service.get_spec_or_404(session=session, spec_id=spec_id)
    
    # Return the raw JSON content
    # Add validation/transformation later if needed before returning
    if isinstance(spec.content, dict):
        return spec.content
    else:
        # Handle cases where content might not be a dict (shouldn't happen with model)
        raise HTTPException(status_code=500, detail="Invalid spec content format") 