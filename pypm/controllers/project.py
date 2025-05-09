from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table

from pypm.console import console
from pypm.db import Project
from pypm.services.project import ProjectService


def project_panel(project: Project):
    """
    Return a rich.panel.Panel of the project details.
    """
    panel_group = Group(
        f"[bold]ID:[/bold] {project.id}",
        f"[bold]Name:[/bold] {project.name}",
        f"[bold]Slug:[/bold] {project.slug}",
        f"[bold]Created At:[/bold] {project.created_at}",
        f"[bold]Updated At:[/bold] {project.updated_at}",
        f"[bold]Status:[/bold] {project.status}",
    )

    return Panel(panel_group)


class ProjectController:
    @staticmethod
    def create(args):
        project = ProjectService.create(args.name)
        console.print("[green]Project created successfully![/green]")
        console.print(project_panel(project))

    @staticmethod
    def list(args):
        projects = ProjectService.list()

        if len(projects) > 0:
            table = Table(title="Projects")

            table.add_column("ID", justify="center", style="cyan")
            table.add_column("Name", justify="left", style="magenta")
            table.add_column("Slug", justify="left", style="green")
            table.add_column("Status", justify="left", style="yellow")

            for project in projects:
                table.add_row(
                    str(project.id),
                    project.name,
                    project.slug,
                    project.status,
                )

            console.print(table)
        else:
            console.print("[yellow]No projects found.[/yellow]")

    @staticmethod
    def get(args):
        project = ProjectService.get_by_slug(args.slug)
        console.print(project_panel(project))

    @staticmethod
    def update(args):
        kwargs = {}

        if args.name:
            kwargs["name"] = args.name
        if args.status:
            kwargs["status"] = args.status

        updated = ProjectService.update(args.slug, **kwargs)
        console.print("[green]Project updated successfully![/green]")
        console.print(project_panel(updated))

    @staticmethod
    def delete(args):
        ProjectService.delete(args.slug)
        console.print(f"[green]Project deleted successfully![/green]")
