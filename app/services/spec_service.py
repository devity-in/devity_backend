import uuid
from typing import Optional

from fastapi import HTTPException, Depends
from sqlmodel import Session, select

from app.database.database import get_db
from app.database.models.spec import Spec, SpecCreate, SpecUpdate


def create_spec(*, session: Session = Depends(get_db), spec_in: SpecCreate) -> Spec:
    """Creates a new Spec in the database."""
    # Create a Spec instance from the input schema
    # project_id might need validation later
    db_spec = Spec.model_validate(spec_in) 
    session.add(db_spec)
    session.commit()
    session.refresh(db_spec)
    return db_spec

def get_spec(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> Optional[Spec]:
    """Gets a single Spec by its ID."""
    statement = select(Spec).where(Spec.id == spec_id)
    spec = session.exec(statement).first()
    return spec

def get_spec_or_404(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> Spec:
    """Gets a single Spec by its ID, raising HTTPException 404 if not found."""
    spec = get_spec(session=session, spec_id=spec_id)
    if not spec:
        raise HTTPException(status_code=404, detail=f"Spec with id {spec_id} not found")
    return spec

def update_spec(
    *, 
    session: Session = Depends(get_db), 
    spec_id: uuid.UUID, 
    spec_in: SpecUpdate
) -> Spec:
    """Updates an existing Spec."""
    db_spec = get_spec_or_404(session=session, spec_id=spec_id)
    
    # Get update data, excluding unset fields to avoid overwriting with None
    update_data = spec_in.model_dump(exclude_unset=True)
    
    # Update the model fields
    db_spec.sqlmodel_update(update_data)

    session.add(db_spec)
    session.commit()
    session.refresh(db_spec)
    return db_spec

# Optional: Add delete_spec if needed for M1
# def delete_spec(*, session: Session = Depends(get_db), spec_id: uuid.UUID) -> None:
#     """Deletes a spec."""
#     db_spec = get_spec_or_404(session=session, spec_id=spec_id)
#     session.delete(db_spec)
#     session.commit()
#     return 