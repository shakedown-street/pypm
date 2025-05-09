from pypm.db import Session, Task
from pypm.services.project import ProjectService


class TaskService:
    @staticmethod
    def create(project_slug, title, *args, **kwargs):
        """
        Create a new task for the specified project in the database
        and return it.
        """
        project = ProjectService.get_by_slug(project_slug)
        if not project:
            raise ValueError(f"Project with slug '{project_slug}' not found.")

        with Session() as session:
            task = Task(
                project_id=project.id,
                title=title,
                **kwargs,
            )

            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def list(project_slug=None):
        """
        List all tasks in the database, optionally filtered by project slug.
        """
        with Session() as session:
            if project_slug:
                project = ProjectService.get_by_slug(project_slug)
                if not project:
                    raise ValueError(f"Project with slug '{project_slug}' not found.")
                tasks = (
                    session.query(Task)
                    .filter_by(project_id=project.id)
                    .order_by(Task.created_at.desc())
                    .all()
                )
            else:
                tasks = session.query(Task).order_by(Task.created_at.desc()).all()
            return tasks

    @staticmethod
    def get(id):
        """
        Get a task from the database by `id`.
        """
        with Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            return task

    @staticmethod
    def update(id, **kwargs):
        """
        Update fields of a task in the database by `id`
        and return the updated task.
        """
        with Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            if not task:
                return None

            for key, value in kwargs.items():
                setattr(task, key, value)

            session.commit()
            session.refresh(task)
            return task

    @staticmethod
    def delete(id):
        """
        Delete a task from the database by `id`
        and return the deleted task.
        """
        with Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            if not task:
                return None

            session.delete(task)
            session.commit()
            return task
