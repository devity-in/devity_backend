import uuid
from typing import Optional, List, Dict, Any

from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from app.database.database import get_db
from app.database.models.spec import Spec # Use the DB model
# from app.database.models.spec import SpecCreate, SpecUpdate # Old schemas not used directly
from app.schemas.spec_schema import Spec as SpecSchema # Our new comprehensive schema


def create_spec(
    *,
    session: Session = Depends(get_db),
    # project_id: uuid.UUID, # Removed: now part of spec_in
    spec_in: SpecSchema
) -> Spec: # Return the DB model instance
    """Creates a new Spec in the database, storing content as JSON."""
    # TODO: Add validation if a spec with spec_in.specId already exists for this project?
    db_spec = Spec(
        project_id=spec_in.project_id, # Get from spec_in
        # Extract metadata? Or store everything in content?
        # For simplicity, store the whole input schema in content for now.
        # We might optimize later to store key metadata in separate columns.
        content=spec_in.model_dump()
    )
    session.add(db_spec)
    session.commit()
    session.refresh(db_spec)
    return db_spec

def get_spec(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> Optional[Spec]:
    """Gets a single Spec DB record by its ID."""
    # Assuming spec_id route parameter corresponds to the primary key (UUID)
    statement = select(Spec).where(Spec.id == spec_id)
    spec = session.exec(statement).first()
    return spec

def get_spec_content_or_404(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> Dict[str, Any]:
    """Gets the content dictionary of a Spec by its ID, raising 404 if not found."""
    db_spec = get_spec(session=session, spec_id=spec_id)
    if not db_spec:
        raise HTTPException(status_code=404, detail=f"Spec with id {spec_id} not found")
    # Return the content field, which is already a dictionary
    # FastAPI will use the route's response_model (SpecSchema) to validate/serialize this dict
    return db_spec.content

def update_spec(
    *,
    session: Session = Depends(get_db),
    spec_id: uuid.UUID, # Assuming spec_id route param is the UUID PK
    spec_in: SpecSchema
) -> Spec: # Return the updated DB model instance
    """Updates an existing Spec's content field."""
    db_spec = get_spec_or_404(session=session, spec_id=spec_id)

    # Overwrite the entire content field with the new spec schema
    db_spec.content = spec_in.model_dump()

    session.add(db_spec)
    session.commit()
    session.refresh(db_spec)
    return db_spec

# --- Renamed function used by GET route --- #
def get_spec_or_404(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> Dict[str, Any]:
    """Gets Spec content or 404. Wrapper for get_spec_content_or_404."""
    # Route expects the content dictionary matching SpecSchema
    return get_spec_content_or_404(session=session, spec_id=spec_id)


# Function to get multiple specs (summary) remains the same
def get_specs_for_project(
    *,
    session: Session = Depends(get_db),
    project_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100
) -> List[Spec]: # Still returns DB models (caller might convert to summary)
    """Gets a list of specs associated with a specific project_id."""
    statement = select(Spec).where(Spec.project_id == project_id).offset(skip).limit(limit)
    specs = session.exec(statement).all()
    return specs

# Delete function remains the same structurally
# def delete_spec(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> None:
#     """Deletes a spec."""
#     db_spec = get_spec_or_404(session=session, spec_id=spec_id)
#     session.delete(db_spec)
#     session.commit()
#     return
