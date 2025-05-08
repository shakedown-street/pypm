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
        try:
            project_slug = args.project
            tasks = self.task_service.list(project_slug)

            if project_slug:
                console.print(f"[bold]Tasks for Project '{project_slug}':[/bold]")
            else:
                console.print("[bold]All Tasks:[/bold]")

            if tasks:
                for task in tasks:
                    console.print(
                        f"- [cyan]{task.title}[/cyan] (ID: {task.id}, Status: {task.status}, Priority: {task.priority})"
                    )
                    console.print(f"\tCreated At: {task.created_at}")
                    if task.due_date:
                        console.print(f"\tDue Date: {task.due_date}")
            else:
                console.print(f"[yellow]No tasks found[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def get(self, args):
        try:
            id = args.id
            task = self.task_service.get(id)

            if task:
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
            else:
                console.print(f"[yellow]Task with ID '{id}' not found.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def update(self, args):
        try:
            task = self.task_service.get(args.id)
            if not task:
                console.print(f"[red]Task with ID '{args.id}' not found.[/red]")
                return
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
            updated = self.task_service.update(task.id, **kwargs)
            if updated:
                console.print(
                    f"[green]Task '{task.title}' updated successfully![/green]"
                )
            else:
                console.print(f"[red]Failed to update task.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def delete(self, args):
        try:
            deleted = self.task_service.delete(args.id)
            if deleted:
                console.print(
                    f"[green]Task '{deleted.title}' deleted successfully![/green]"
                )
            else:
                console.print(f"[red]Failed to delete task.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
