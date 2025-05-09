from slugify import slugify

from pypm.db import Project, Session


class ProjectService:
    @staticmethod
    def create(name: str) -> Project:
        """
        Create a new project in the database and return it.
        """
        with Session() as session:
            slug = slugify(name)
            project = Project(name=name, slug=slug)

            session.add(project)
            session.commit()
            session.refresh(project)

            return project

    @staticmethod
    def list() -> list[Project]:
        """
        List all projects in the database.
        """
        with Session() as session:
            projects = session.query(Project).order_by(Project.name.asc()).all()
            return projects

    @staticmethod
    def get(id: int) -> Project | None:
        """
        Get a project from the database by `id`.
        """
        with Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            return project

    @staticmethod
    def get_by_slug(slug: str) -> Project | None:
        """
        Get a project from the database by `slug`.
        """
        with Session() as session:
            project = session.query(Project).filter_by(slug=slug).first()
            return project

    @staticmethod
    def update(id: int, **kwargs) -> Project:
        """
        Update fields of a project in the database by `id`
        and return the updated project.
        """
        with Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            if not project:
                raise ValueError(f"Project not found.")

            project.name = kwargs.get("name", project.name)
            project.slug = slugify(kwargs.get("name", project.name))
            project.status = kwargs.get("status", project.status)

            session.commit()
            session.refresh(project)

            return project

    @staticmethod
    def delete(id: int) -> Project:
        """
        Delete a project from the database by `id` and return the deleted project.
        """
        with Session() as session:
            project = session.query(Project).filter_by(id=id).first()
            if not project:
                raise ValueError(f"Project not found.")

            session.delete(project)
            session.commit()

            return project
