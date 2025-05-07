from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

DB_NAME = "pypm.db"


Base = declarative_base()

engine = create_engine(f"sqlite:///{DB_NAME}")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    status = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="project")

    def __repr__(self):
        return f"<Project(name={self.name}, slug={self.slug}, status={self.status})>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )
    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title={self.title}, status={self.status}, priority={self.priority})>"


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
