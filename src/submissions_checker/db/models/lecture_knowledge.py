"""Lecture knowledge content for RAG-based AI reviews."""

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from submissions_checker.db.models.base import Base, TimestampMixin


class LectureKnowledge(Base, TimestampMixin):
    """Stores lecture theory content indexed by lab ID for use in AI reviews."""

    __tablename__ = "lecture_knowledge"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lab_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
