from pypm.console import console
from pypm.services.project import ProjectService


class ProjectController:
    def create(self, args):
        try:
            project = ProjectService.create(args.name)
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
            projects = ProjectService.list()

            if projects:
                console.print("[bold]Projects:[/bold]")
                for project in projects:
                    console.print(
                        f"- [cyan]{project.name}[/cyan] (ID: {project.id}, Slug: {project.slug})"
                    )
            else:
                console.print("[yellow]No projects found.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def get(self, args):
        try:
            project = ProjectService.get_by_slug(args.slug)
            if project:
                console.print(f"[bold]Project:[/bold] {project.name}")
                console.print(f"[bold]ID:[/bold] {project.id}")
                console.print(f"[bold]Slug:[/bold] {project.slug}")
                console.print(f"[bold]Created At:[/bold] {project.created_at}")
                console.print(f"[bold]Updated At:[/bold] {project.updated_at}")
                console.print(f"[bold]Status:[/bold] {project.status}")
            else:
                console.print("[red]Project not found.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def update(self, args):
        try:
            project = ProjectService.get_by_slug(args.slug)
            if not project:
                console.print("[red]Project not found.[/red]")
                return

            kwargs = {}

            if args.name:
                kwargs["name"] = args.name
            if args.status:
                kwargs["status"] = args.status

            updated = ProjectService.update(project.id, **kwargs)
            if updated:
                console.print(
                    f"[green]Project '{updated.name}' updated successfully![/green]"
                )
            else:
                console.print("[red]Failed to update project.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def delete(self, args):
        try:
            project = ProjectService.get_by_slug(args.slug)
            if not project:
                console.print("[red]Project not found.[/red]")
                return
            deleted = ProjectService.delete(project.id)
            if deleted:
                console.print(
                    f"[green]Project '{deleted.name}' deleted successfully![/green]"
                )
            else:
                console.print("[red]Failed to delete project.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
