import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlmodel import Field, SQLModel, JSON, Column


class SpecBase(SQLModel):
    # Assuming project_id links to a Project model (TBD)
    # Making it optional for now until Project model is created
    # project_id: Optional[str] = Field(index=True, foreign_key="project.id") # Commented out for M1
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

    # Define relationships later if needed, e.g.:
    # project: Optional["Project"] = Relationship(back_populates="specs")


class SpecCreate(SpecBase):
    # Potentially add fields required only on creation
    pass


class SpecUpdate(SQLModel):
    # Only content is updatable for now
    content: Optional[Dict[str, Any]] = None


class SpecRead(SpecBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime 