from slugify import slugify
from sqlalchemy.exc import IntegrityError

from pypm.console import console
from pypm.db import Project, Session


class ProjectController:
    def create(self, args):
        """
        Create a new project with the given name.
        """
        name = args.name
        slug = slugify(args.name)
        status = "active"

        new_project = Project(
            name=name,
            slug=slug,
            status=status,
        )

        try:
            session = Session()
            session.add(new_project)
            session.commit()
            console.print(f"[green]Project '{name}' created successfully![/green]")
        except IntegrityError:
            session.rollback()
            console.print(
                f"[red]Error: A project with the slug '{slug}' already exists.[/red]"
            )
        finally:
            session.close()

    def list(self, args):
        """
        List all projects.
        """
        try:
            session = Session()
            projects = session.query(Project).all()

            if projects:
                console.print("[bold]Projects:[/bold]")
                for project in projects:
                    console.print(
                        f"- [cyan]{project.name}[/cyan] (Slug: {project.slug}, Status: {project.status})"
                    )
            else:
                console.print("[yellow]No projects found.[/yellow]")
        finally:
            session.close()
