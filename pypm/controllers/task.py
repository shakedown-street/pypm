from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from pypm.console import console
from pypm.db import Task
from pypm.services.task import TaskService


def task_panel(task: Task):
    """
    Return a rich.panel.Panel of the task details.
    """
    panel_group = Group(
        f"[bold]ID:[/bold] {task.id}",
        f"[bold]Title:[/bold] {task.title}",
        f"[bold]Project ID:[/bold] {task.project_id}",
        f"[bold]Priority:[/bold] {task.priority}",
        f"[bold]Status:[/bold] {task.status}",
        f"[bold]Created At:[/bold] {task.created_at}",
        f"[bold]Updated At:[/bold] {task.updated_at}",
        f"[bold]Due Date:[/bold] {task.due_date}",
        f"[bold]Body:[/bold]\n{task.body}",
    )

    return Panel(panel_group)


class TaskController:
    @staticmethod
    def create(args):
        project_slug = args.project_slug
        title = args.title

        kwargs = {}
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
        console.print("[green]Task created successfully![/green]")
        console.print(task_panel(task))

    @staticmethod
    def list(args):
        project_slug = args.project
        tasks = TaskService.list(project_slug)

        if len(tasks) > 0:
            table = Table(
                title="Tasks" if not project_slug else f"Tasks for '{project_slug}'"
            )

            table.add_column("ID", justify="center", style="cyan")
            table.add_column("Title", justify="left", style="magenta")
            table.add_column("Created At", justify="left", style="blue")
            table.add_column("Due Date", justify="left", style="blue")
            table.add_column("Priority", justify="left", style="green")
            table.add_column("Status", justify="left", style="yellow")

            for task in tasks:
                table.add_row(
                    str(task.id),
                    task.title,
                    task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
                    task.priority,
                    task.status,
                )

            console.print(table)
        else:
            console.print("[yellow]No tasks found.[/yellow]")

    @staticmethod
    def get(args):
        id = args.id
        task = TaskService.get(id)
        console.print(task_panel(task))

    @staticmethod
    def update(args):
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

        updated = TaskService.update(args.id, **kwargs)
        console.print("[green]Task updated successfully![/green]")
        console.print(task_panel(updated))

    @staticmethod
    def delete(args):
        TaskService.delete(args.id)
        console.print(f"[green]Task deleted successfully![/green]")
