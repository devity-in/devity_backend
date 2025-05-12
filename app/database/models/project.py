import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

# Forward reference for relationship typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .spec import Spec # Assuming Spec model is in spec.py

class ProjectBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    # Add other project-related fields later, e.g., owner_id

class Project(ProjectBase, table=True):
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

    # Define the one-to-many relationship with Spec
    specs: List["Spec"] = Relationship(back_populates="project")

# --- Pydantic Schemas for API --- 

class ProjectCreate(ProjectBase):
    # Fields required on creation
    pass 

class ProjectUpdate(SQLModel):
    # Fields allowed for update
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    # Fields returned when reading a project
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # Optionally include related specs if needed in the future
    # specs: List["SpecRead"] = [] # Assuming SpecRead exists 