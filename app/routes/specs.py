import uuid
from typing import List # Add List import

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Import schemas and service functions
from app.database.models.spec import SpecRead, SpecCreate, SpecUpdate
from app.services import spec_service
from app.database.database import get_db

# Create the router
router = APIRouter()

@router.post("/", response_model=SpecRead, status_code=201)
def create_new_spec(
    *, 
    session: Session = Depends(get_db), 
    spec_in: SpecCreate
) -> SpecRead:
    """Create a new spec entry.

    Args:
        session: Database session dependency.
        spec_in: Input data schema.

    Returns:
        The created spec data.
    """
    # For M1, project_id might be null initially if not provided
    # Add project validation/lookup here later
    spec = spec_service.create_spec(session=session, spec_in=spec_in)
    return spec

@router.put("/{spec_id}", response_model=SpecRead)
def update_existing_spec(
    *, 
    session: Session = Depends(get_db), 
    spec_id: uuid.UUID,
    spec_in: SpecUpdate
) -> SpecRead:
    """Update an existing spec's content.

    Args:
        session: Database session dependency.
        spec_id: The UUID of the spec to update.
        spec_in: Input data schema with updated content.

    Returns:
        The updated spec data.
    
    Raises:
        HTTPException: 404 if spec not found.
    """
    # get_spec_or_404 is implicitly called by update_spec
    updated_spec = spec_service.update_spec(session=session, spec_id=spec_id, spec_in=spec_in)
    return updated_spec

# Placeholder for GET endpoint (maybe needed later, not strictly for M1 commit 4)
# @router.get("/{spec_id}", response_model=SpecRead)
# def read_spec(
#     *, 
#     session: Session = Depends(get_db),
#     spec_id: uuid.UUID
# ) -> SpecRead:
#     """Get a specific spec by ID."""
#     spec = spec_service.get_spec_or_404(session=session, spec_id=spec_id)
#     return spec

# Placeholder for GET list endpoint (maybe needed later)
# @router.get("/", response_model=List[SpecRead])
# def read_specs(
#     *, 
#     session: Session = Depends(get_db),
#     skip: int = 0,
#     limit: int = 100
# ) -> List[SpecRead]:
#     """Retrieve multiple specs."""
#     # Add service function for listing specs later
#     # specs = spec_service.get_specs(session=session, skip=skip, limit=limit)
#     # return specs
#     pass 