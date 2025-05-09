from pypm.console import console
from pypm.services.task import TaskService


class TaskController:
    @staticmethod
    def create(args):
        project_slug = args.project_slug
        title = args.title

        kwargs = {}
        if args.body:
            kwargs["body"] = args.body
        if args.status:
            kwargs["status"] = args.status
        if args.priority:
            kwargs["priority"] = args.priority
        if args.due_date:
            kwargs["due_date"] = args.due_date

        task = TaskService.create(
            project_slug,
            title,
            **kwargs,
        )
        console.print(f"[green]Task '{task.title}' created successfully![/green]")

    @staticmethod
    def list(args):
        project_slug = args.project
        tasks = TaskService.list(project_slug)

        if project_slug:
            console.print(f"[bold]Tasks for '{project_slug}':[/bold]")
        else:
            console.print("[bold]Tasks:[/bold]")

        if len(tasks) > 0:
            for task in tasks:
                console.print(
                    f"- [cyan]{task.title}[/cyan] (ID: {task.id}, Status: {task.status}, Priority: {task.priority})"
                )
        else:
            console.print(f"[yellow]No tasks found[/yellow]")

    @staticmethod
    def get(args):
        id = args.id
        task = TaskService.get(id)
        console.print(
            f"[bold]Task:[/bold] {task.title}\n"
            f"[bold]ID:[/bold] {task.id}\n"
            f"[bold]Project ID:[/bold] {task.project_id}\n"
            f"[bold]Created At:[/bold] {task.created_at}\n"
            f"[bold]Updated At:[/bold] {task.updated_at}\n"
            f"[bold]Due Date:[/bold] {task.due_date}\n"
            f"[bold]Priority:[/bold] {task.priority}\n"
            f"[bold]Status:[/bold] {task.status}\n"
            f"{task.body}\n"
        )

    @staticmethod
    def update(args):
        task = TaskService.get(args.id)

        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.body:
            kwargs["body"] = args.body
        if args.status:
            kwargs["status"] = args.status
        if args.priority:
            kwargs["priority"] = args.priority
        if args.due_date:
            kwargs["due_date"] = args.due_date

        updated = TaskService.update(task.id, **kwargs)
        console.print(f"[green]Task '{updated.title}' updated successfully![/green]")

    @staticmethod
    def delete(args):
        deleted = TaskService.delete(args.id)
        console.print(f"[green]Task '{deleted.title}' deleted successfully![/green]")
