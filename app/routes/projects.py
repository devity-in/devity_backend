import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Import schemas, service, and db dependency
from app.database.models.project import ProjectRead, ProjectCreate # Add ProjectUpdate if needed
from app.database.models.spec import SpecSummaryRead
from app.services import project_service
from app.services import spec_service # Import spec_service
from app.database.database import get_db

# Create the router
router = APIRouter()

@router.post("/", response_model=ProjectRead, status_code=201)
def create_new_project(
    *,
    session: Session = Depends(get_db),
    project_in: ProjectCreate
) -> ProjectRead:
    """Create a new project."""
    project = project_service.create_project(session=session, project_in=project_in)
    return project

@router.get("/", response_model=List[ProjectRead])
def read_projects_list(
    *,
    session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> List[ProjectRead]:
    """Retrieve a list of projects."""
    projects = project_service.get_projects(session=session, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=ProjectRead)
def read_single_project(
    *,
    session: Session = Depends(get_db),
    project_id: uuid.UUID
) -> ProjectRead:
    """Get a specific project by its ID."""
    project = project_service.get_project_or_404(session=session, project_id=project_id)
    return project

# --- Endpoint to get specs for a project ---

@router.get("/{project_id}/specs", response_model=List[SpecSummaryRead])
def read_project_specs(
    *,
    session: Session = Depends(get_db),
    project_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100
) -> List[SpecSummaryRead]:
    """Retrieve a list of specs belonging to a specific project."""
    # Optional: Verify project exists first using project_service.get_project_or_404 if needed
    specs = spec_service.get_specs_for_project(
        session=session, project_id=project_id, skip=skip, limit=limit
    )
    # Note: get_specs_for_project returns List[Spec], but FastAPI handles the
    # conversion to List[SpecSummaryRead] based on the response_model.
    return specs

# Optional: Add PUT/DELETE endpoints later if needed for M2
# @router.put("/{project_id}", response_model=ProjectRead)
# def update_existing_project(...):
#     ...
#
# @router.delete("/{project_id}", status_code=204) # No content on successful delete
# def delete_existing_project(...):
#     ...
