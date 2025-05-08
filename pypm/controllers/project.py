from pypm.console import console
from pypm.services.project import ProjectService


class ProjectController:
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def create(self, args):
        try:
            project = self.project_service.create(args.name)
            if project:
                console.print(
                    f"[green]Project '{project.name}' created successfully with slug '{project.slug}'![/green]"
                )
            else:
                console.print("[red]Failed to create project.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def list(self, args):
        try:
            projects = self.project_service.list()

            if projects:
                console.print("[bold]Projects:[/bold]")
                for project in projects:
                    console.print(
                        f"- [cyan]{project.name}[/cyan] (Slug: {project.slug})"
                    )
            else:
                console.print("[yellow]No projects found.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
