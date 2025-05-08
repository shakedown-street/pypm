from slugify import slugify

from pypm.db import Database, Project


class ProjectService:
    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str):
        with self.db.Session() as session:
            slug = slugify(name)
            project = Project(name=name, slug=slug)

            session.add(project)
            session.commit()
            session.refresh(project)

            return project

    def list(self):
        with self.db.Session() as session:
            projects = session.query(Project).all()
            return projects

    def get_by_slug(self, slug: str):
        with self.db.Session() as session:
            project = session.query(Project).filter_by(slug=slug).first()
            return project
