from pypm.console import console
from pypm.services.task import TaskService


class TaskController:
    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    def create(self, args):
        project_slug = args.project_slug
        title = args.title
        body = args.body
        status = args.status
        priority = args.priority
        due_date = args.due_date

        try:
            self.task = self.task_service.create(
                project_slug,
                title,
                body=body,
                status=status,
                priority=priority,
                due_date=due_date,
            )
            console.print(f"[green]Task '{title}' created successfully![/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def list(self, args):
        """
        List all tasks for a given project.
        """
        project_slug = args.project_slug

        try:
            tasks = self.task_service.list(project_slug)

            if tasks:
                console.print(f"[bold]Tasks for Project '{project_slug}':[/bold]")
                for task in tasks:
                    console.print(
                        f"- [cyan]{task.title}[/cyan] (Status: {task.status}, Priority: {task.priority})"
                    )
            else:
                console.print(
                    f"[yellow]No tasks found for project '{project_slug}'.[/yellow]"
                )
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
