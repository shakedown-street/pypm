from pypm.db import Database, Task
from pypm.services.project import ProjectService


class TaskService:
    def __init__(self, db: Database, project_service: ProjectService):
        self.db = db
        self.project_service = project_service

    def create(self, project_slug, title, *args, **kwargs):
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

    def list(self, project_slug):
        project = self.project_service.get_by_slug(project_slug)
        if not project:
            raise ValueError(f"Project with slug '{project_slug}' not found.")

        with self.db.Session() as session:
            tasks = (
                session.query(Task)
                .filter_by(project_id=project.id)
                .order_by(Task.created_at.desc())
                .all()
            )

            return tasks
