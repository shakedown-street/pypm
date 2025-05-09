from pypm.db import Database, Task
from pypm.services.project import ProjectService


class TaskService:
    def __init__(self, db: Database, project_service: ProjectService):
        self.db = db
        self.project_service = project_service

    def create(self, project_slug, title, *args, **kwargs):
        """
        Create a new task for the specified project in the database
        and return it.
        """
        project = self.project_service.get_by_slug(project_slug)
        if not project:
            raise ValueError(f"Project with slug '{project_slug}' not found.")

        with self.db.Session() as session:
            task = Task(
                project_id=project.id,
                title=title,
                **kwargs,
            )

            session.add(task)
            session.commit()
            session.refresh(task)
            return task

    def list(self, project_slug=None):
        """
        List all tasks in the database, optionally filtered by project slug.
        """
        with self.db.Session() as session:
            if project_slug:
                project = self.project_service.get_by_slug(project_slug)
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

    def get(self, id):
        """
        Get a task from the database by `id`.
        """
        with self.db.Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            return task

    def update(self, id, **kwargs):
        """
        Update fields of a task in the database by `id`
        and return the updated task.
        """
        with self.db.Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            if not task:
                return None

            for key, value in kwargs.items():
                setattr(task, key, value)

            session.commit()
            session.refresh(task)
            return task

    def delete(self, id):
        """
        Delete a task from the database by `id`
        and return the deleted task.
        """
        with self.db.Session() as session:
            task = session.query(Task).filter_by(id=id).first()
            if not task:
                return None

            session.delete(task)
            session.commit()
            return task
