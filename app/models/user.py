from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.enums.enums import UserRole

if TYPE_CHECKING:
    from app.models.classroom import Classroom
    from app.models.academic import AcademicResult


class User(Base):
    """
    Unified User model representing both Students and Teachers/Admins.
    Holds primary authentication credentials, role flags, personal profile details,
    and student-specific assignments.
    """

    __tablename__ = "users"

    # Primary Identifier
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, comment="Unique primary key for the user account"
    )

    # Core Authentication & System Fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="Unique email address used for system login",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Argon2/Bcrypt hashed password string"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.STUDENT,
        nullable=False,
        comment="System role determining permissions (e.g., ADMIN, TEACHER, STUDENT)",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Flag to activate/deactivate account access",
    )

    # General User Profile Details (Shared by Teachers and Students)
    first_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="User's legal first name"
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, comment="User's legal last name"
    )
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, comment="Primary contact telephone number"
    )
    bio: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True, comment="Short biography or professional/academic notes"
    )

    classroom_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("classrooms.id", ondelete="SET NULL"),
        nullable=True,
        comment="Foreign key referencing the classroom the student currently belongs to",
    )

    # Audit Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp when the user account was registered",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when the user profile was last updated",
    )

    # ORM Relationships
    # Many-to-One: Many students can belong to a single Classroom
    classroom: Mapped[Optional["Classroom"]] = relationship(
        "Classroom", back_populates="students", foreign_keys=[classroom_id]
    )

    # One-to-Many (or One-to-One): Links a teacher to the classroom(s) they manage via Classroom.teacher_id
    managed_class: Mapped[Optional["Classroom"]] = relationship(
        "Classroom", back_populates="teacher", foreign_keys="Classroom.teacher_id"
    )

    # One-to-Many: A student can have multiple AcademicResults; deletes orphaned results automatically
    results: Mapped[List["AcademicResult"]] = relationship(
        "AcademicResult", back_populates="student", cascade="all, delete-orphan"
    )
