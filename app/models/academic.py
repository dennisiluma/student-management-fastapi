from datetime import datetime
from typing import Dict, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Enum, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.enums.enums import GradeTerm

if TYPE_CHECKING:
    from app.models.user import User


class AcademicResult(Base):
    """
    AcademicResult model representing a student's full term report card.
    Stores subjects and grades collectively in a JSON payload.
    """
    __tablename__ = "academic_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    term: Mapped[GradeTerm] = mapped_column(
        Enum(GradeTerm, native_enum=False), nullable=False
    )
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Store subject -> grade mapping, e.g., {"Maths": "A", "English": "B"}
    grades: Mapped[Dict[str, str]] = mapped_column(
        JSON, nullable=False, default=dict
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    student: Mapped["User"] = relationship("User", back_populates="results")