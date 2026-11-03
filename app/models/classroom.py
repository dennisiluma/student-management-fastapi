from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Classroom(Base):
    """
    Classroom model representing a school class or grade room.
    Links a managing Teacher user to enrolled Student users.
    """

    __tablename__ = "classrooms"

    # Primary Identifier
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment="Unique primary key for the classroom"
    )

    # Classroom Attributes
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="Unique name/title of the classroom (e.g., Grade 10 A, Maths 101)",
    )

    teacher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_classrooms_teacher_id_users",
        ),
        unique=True,  # Guarantees a teacher cannot manage more than one classroom in the database
        nullable=True,
        comment="Foreign key referencing the Teacher assigned to manage this classroom",
    )

    # Audit Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp when the classroom record was created",
    )

    # ORM Relationships
    # One-to-One (or One-to-Many depending on business logic constraints): Links this classroom to its managing teacher via teacher_id
    teacher: Mapped[Optional["User"]] = relationship(
        "User", back_populates="managed_class", foreign_keys=[teacher_id]
    )

    # One-to-Many: A single classroom can contain multiple students linked via User.classroom_id
    students: Mapped[List["User"]] = relationship(
        "User", back_populates="classroom", foreign_keys="User.classroom_id"
    )
