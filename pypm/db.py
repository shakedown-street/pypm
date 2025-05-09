import datetime

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    status: Mapped[str] = mapped_column(nullable=False, default="active")
    tasks: Mapped["Task"] = relationship(back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(nullable=False)
    priority: Mapped[str] = mapped_column(nullable=False)
    due_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    project: Mapped[Project] = relationship(back_populates="tasks")


engine = create_engine(f"sqlite:///pypm.db")
Session = sessionmaker(bind=engine)


def init_db():
    """Initialize the database and create tables."""
    Base.metadata.create_all(engine)
