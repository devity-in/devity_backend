import uuid
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

# Import Project models
from app.database.models.project import Project, ProjectCreate, ProjectUpdate


def create_project(session: Session, project_in: ProjectCreate) -> Project:
    """Create a new project in the database."""
    # Check for duplicates maybe?
    db_project = Project.model_validate(project_in)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def get_project(session: Session, project_id: uuid.UUID) -> Optional[Project]:
    """Get a single project by its ID."""
    statement = select(Project).where(Project.id == project_id)
    project = session.exec(statement).first()
    return project

def get_project_or_404(session: Session, project_id: uuid.UUID) -> Project:
    """Get a single project by its ID, raising 404 if not found."""
    project = get_project(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    return project

def get_projects(session: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    """Get a list of projects, with pagination."""
    statement = select(Project).offset(skip).limit(limit)
    projects = session.exec(statement).all()
    return projects

# Optional: Add update/delete functions later if needed for M2
# def update_project(session: Session, project_id: uuid.UUID, project_in: ProjectUpdate) -> Project:
#     ...
# 
# def delete_project(session: Session, project_id: uuid.UUID) -> None:
#     ... 