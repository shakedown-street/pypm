import sqlite3

from pypika import Query, Table
from slugify import slugify

from pypm.console import console
from pypm.db import get_connection


class ProjectController:
    def create(self, args):
        """
        Create a new project with the given name.
        """
        connection = get_connection()
        cursor = connection.cursor()

        projects_table = Table("projects")

        name = args.name
        slug = slugify(args.name)
        status = "active"

        q = (
            Query.into(projects_table)
            .columns("name", "slug", "status")
            .insert(name, slug, status)
        )

        try:
            cursor.execute(str(q))
            connection.commit()
            console.print(f"[green]Project '{args.name}' created successfully![/green]")
        except sqlite3.IntegrityError as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            connection.close()

    def list(self, args):
        """
        List all projects.
        """
        connection = get_connection()
        cursor = connection.cursor()

        projects_table = Table("projects")
        q = Query.from_(projects_table).select("id", "name", "slug", "status")

        cursor.execute(str(q))
        rows = cursor.fetchall()

        if rows:
            console.print("[bold]Projects:[/bold]")
            for row in rows:
                console.print(
                    f"- [cyan]{row[1]}[/cyan] (Slug: {row[2]}, Status: {row[3]})"
                )
        else:
            console.print("[yellow]No projects found.[/yellow]")

        connection.close()
