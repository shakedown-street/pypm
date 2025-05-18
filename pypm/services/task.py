from pypm.db import Task, db
from pypm.services.project import ProjectService


class TaskService:
    @staticmethod
    def create(project_slug, title, **kwargs) -> Task:
        """
        Create a new task for the specified project in the database
        and return it.
        """
        project = ProjectService.get_by_slug(project_slug)

        with db.atomic():
            task = Task.create(
                project_id=project.id,
                title=title,
                **kwargs,
            )

            return task

    @staticmethod
    def list(project_slug=None) -> list[Task]:
        """
        List all tasks in the database, optionally filtered by project slug.
        """
        if project_slug:
            project = ProjectService.get_by_slug(project_slug)
            if not project:
                raise ValueError(f"Project with slug '{project_slug}' not found.")

            tasks = (
                Task.select()
                .where(Task.project_id == project.id)
                .order_by(Task.created_at.desc())
            )
        else:
            tasks = Task.select().order_by(Task.created_at.desc())

        return tasks

    @staticmethod
    def get(id) -> Task:
        """
        Get a task from the database by `id`.
        """
        task = Task.get_by_id(id)
        return task

    @staticmethod
    def update(id, **kwargs) -> Task:
        """
        Update fields of a task in the database by `id`
        and return the updated task.
        """
        task = Task.get_by_id(id)

        if not task:
            raise ValueError(f"Task with id '{id}' not found.")

        with db.atomic():
            # Update fields dynamically based on kwargs
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
                else:
                    raise ValueError(f"Invalid field '{key}' for Task.")

            task.save()

        return task

    @staticmethod
    def delete(id) -> Task:
        """
        Delete a task from the database by `id` and return the deleted task.
        """
        with db.atomic():
            task = Task.get_by_id(id)

            if not task:
                raise ValueError(f"Task with id '{id}' not found.")

            task.delete_instance()
            return task
