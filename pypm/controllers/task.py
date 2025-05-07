import sqlite3

from pypika import Query, Table

from pypm.console import console
from pypm.db import get_connection


class TaskController:
    def create(self, args):
        """
        Create a new task.
        """
        connection = get_connection()
        cursor = connection.cursor()

        tasks_table = Table("tasks")

        project_slug = args.project_slug
        title = args.title
        body = args.body
        status = args.status
        priority = args.priority
        due_date = args.due_date

        # Check if the project exists
        project_query = (
            Query.from_(Table("projects"))
            .select("id")
            .where(Table("projects").slug == project_slug)
        )
        cursor.execute(str(project_query))
        project_id = cursor.fetchone()
        if not project_id:
            console.print(
                f"[red]Error: Project with slug '{project_slug}' not found.[/red]"
            )
            return
        project_id = project_id[0]

        q = (
            Query.into(tasks_table)
            .columns("project_id", "title", "body", "status", "priority", "due_date")
            .insert(project_id, title, body, status, priority, due_date)
        )

        try:
            cursor.execute(str(q))
            connection.commit()
            console.print(f"[green]Task '{title}' created successfully![/green]")
        except sqlite3.IntegrityError as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            connection.close()

    def list(self, args):
        """
        List all tasks for a given project.
        """
        connection = get_connection()
        cursor = connection.cursor()

        tasks_table = Table("tasks")
        projects_table = Table("projects")

        project_slug = args.project_slug

        # Check if the project exists
        project_query = (
            Query.from_(projects_table)
            .select("id")
            .where(projects_table.slug == project_slug)
        )
        cursor.execute(str(project_query))
        project_id = cursor.fetchone()
        if not project_id:
            console.print(
                f"[red]Error: Project with slug '{project_slug}' not found.[/red]"
            )
            return
        project_id = project_id[0]

        q = (
            Query.from_(tasks_table)
            .join(projects_table)
            .on(tasks_table.project_id == projects_table.id)
            .select(
                tasks_table.id,
                tasks_table.title,
                tasks_table.status,
                tasks_table.priority,
            )
            .where(projects_table.slug == project_slug)
        )

        cursor.execute(str(q))
        rows = cursor.fetchall()

        if rows:
            console.print(f"[bold]Tasks for Project '{project_slug}':[/bold]")
            for row in rows:
                console.print(
                    f"- [cyan]{row[1]}[/cyan] (Status: {row[2]}, Priority: {row[3]})"
                )
        else:
            console.print(
                f"[yellow]No tasks found for project '{project_slug}'.[/yellow]"
            )

        connection.close()
