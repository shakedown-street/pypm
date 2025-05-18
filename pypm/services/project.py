from slugify import slugify

from pypm.db import Project, db


class ProjectService:
    @staticmethod
    def create(name: str) -> Project:
        """
        Create a new project in the database and return it.
        """
        slug = slugify(name)

        with db.atomic():
            project = Project.create(name=name, slug=slug)

        return project

    @staticmethod
    def list() -> list[Project]:
        """
        List all projects in the database.
        """
        return Project.select().order_by(Project.name.asc())

    @staticmethod
    def get(id: int) -> Project:
        """
        Get a project from the database by `id`.
        """
        project = Project.get_by_id(id)
        return project

    @staticmethod
    def get_by_slug(slug: str) -> Project:
        """
        Get a project from the database by `slug`.
        """
        return Project.get(Project.slug == slug)

    @staticmethod
    def update(slug: str, **kwargs) -> Project:
        """
        Update fields of a project in the database by `slug`
        and return the updated project.
        """
        project = Project.get(Project.slug == slug)

        if not project:
            raise ValueError(f"Project with slug '{slug}' not found.")

        with db.atomic():
            # Update fields dynamically based on kwargs
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
                else:
                    raise ValueError(f"Invalid field '{key}' for Project.")

            project.save()

        return project

    @staticmethod
    def delete(slug: str) -> Project:
        """
        Delete a project from the database by `slug` and return the deleted project.
        """
        with db.atomic():
            project = Project.get(Project.slug == slug)

            if not project:
                raise ValueError(f"Project with slug '{slug}' not found.")

            project.delete_instance()
            return project
