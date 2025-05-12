import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlmodel import Field, SQLModel, JSON, Column, Relationship

# Forward reference for relationship typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .project import Project # Assuming Project model is in project.py


class SpecBase(SQLModel):
    # Link to the Project model via foreign key
    project_id: uuid.UUID = Field(index=True, foreign_key="project.id") 
    # Store the main spec content as JSON
    content: Dict[str, Any] = Field(sa_column=Column(JSON), default={})


class Spec(SpecBase, table=True):
    # Using UUID for the primary key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False
    )

    # Define the many-to-one relationship with Project
    project: Optional["Project"] = Relationship(back_populates="specs")


class SpecCreate(SpecBase):
    # project_id is now required during creation via SpecBase
    pass


class SpecUpdate(SQLModel):
    # Only content is updatable for now
    content: Optional[Dict[str, Any]] = None


class SpecRead(SpecBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # Optionally include project info when reading a spec
    # project: Optional["ProjectRead"] = None # Assuming ProjectRead exists

# New schema for summary list views (excludes content)
class SpecSummaryRead(SQLModel):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime
    updated_at: datetime 