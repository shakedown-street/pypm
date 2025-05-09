from slugify import slugify

from pypm.db import Database, Project


class ProjectService:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str) -> Project:
        with self.db.Session() as session:
            slug = slugify(name)
            project = Project(name=name, slug=slug)

            session.add(project)
            session.commit()
            session.refresh(project)

            return project

    def list(self) -> list[Project]:
        with self.db.Session() as session:
            projects = session.query(Project).order_by(Project.name.asc()).all()
            return projects

    def get(self, id: int) -> Project | None:
        with self.db.Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            return project

    def get_by_slug(self, slug: str) -> Project | None:
        with self.db.Session() as session:
            project = session.query(Project).filter_by(slug=slug).first()
            return project

    def update(self, id: int, **kwargs) -> Project:
        with self.db.Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            if not project:
                raise ValueError(f"Project not found.")

            project.name = kwargs.get("name", project.name)
            project.slug = slugify(kwargs.get("name", project.name))
            project.status = kwargs.get("status", project.status)

            session.commit()
            session.refresh(project)

            return project

    def delete(self, id: int) -> Project:
        with self.db.Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            if not project:
                raise ValueError(f"Project not found.")

            session.delete(project)
            session.commit()

            return project
