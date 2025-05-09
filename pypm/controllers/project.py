from pypm.console import console
from pypm.services.project import ProjectService


class ProjectController:
    @staticmethod
    def create(args):
        project = ProjectService.create(args.name)
        console.print(
            f"[green]Project '{project.name}' created successfully with slug '{project.slug}'![/green]"
        )

    @staticmethod
    def list(args):
        projects = ProjectService.list()

        console.print("[bold]Projects:[/bold]")
        if len(projects) > 0:
            for project in projects:
                console.print(
                    f"- [cyan]{project.name}[/cyan] (ID: {project.id}, Slug: {project.slug})"
                )
        else:
            console.print("[yellow]No projects found.[/yellow]")

    @staticmethod
    def get(args):
        project = ProjectService.get_by_slug(args.slug)
        console.print(f"[bold]Project:[/bold] {project.name}")
        console.print(f"[bold]ID:[/bold] {project.id}")
        console.print(f"[bold]Slug:[/bold] {project.slug}")
        console.print(f"[bold]Created At:[/bold] {project.created_at}")
        console.print(f"[bold]Updated At:[/bold] {project.updated_at}")
        console.print(f"[bold]Status:[/bold] {project.status}")

    @staticmethod
    def update(args):
        project = ProjectService.get_by_slug(args.slug)

        kwargs = {}

        if args.name:
            kwargs["name"] = args.name
        if args.status:
            kwargs["status"] = args.status

        updated = ProjectService.update(project.id, **kwargs)
        console.print(f"[green]Project '{updated.name}' updated successfully![/green]")

    @staticmethod
    def delete(args):
        project = ProjectService.get_by_slug(args.slug)
        deleted = ProjectService.delete(project.id)
        console.print(f"[green]Project '{deleted.name}' deleted successfully![/green]")
