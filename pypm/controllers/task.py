from pypm.console import console
from pypm.db import Project, Session, Task


class TaskController:
    def create(self, args):
        """
        Create a new task.
        """
        project_slug = args.project_slug
        title = args.title
        body = args.body
        status = args.status
        priority = args.priority
        due_date = args.due_date

        # Check if the project exists
        try:
            session = Session()
            project = session.query(Project).filter_by(slug=project_slug).first()
            if not project:
                console.print(
                    f"[red]Error: Project with slug '{project_slug}' not found.[/red]"
                )
                return

            project_id = project.id
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return
        finally:
            session.close()

        # Create the task
        try:
            new_task = Task(
                project_id=project_id,
                title=title,
                body=body,
                status=status,
                priority=priority,
                due_date=due_date,
            )

            session.add(new_task)
            session.commit()
            console.print(f"[green]Task '{title}' created successfully![/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            session.close()

    def list(self, args):
        """
        List all tasks for a given project.
        """
        project_slug = args.project_slug

        # Check if the project exists
        try:
            session = Session()
            project = session.query(Project).filter_by(slug=project_slug).first()
            if not project:
                console.print(
                    f"[red]Error: Project with slug '{project_slug}' not found.[/red]"
                )
                return

            project_id = project.id
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return
        finally:
            session.close()

        # List tasks for the project
        try:
            session = Session()
            tasks = (
                session.query(Task)
                .filter_by(project_id=project_id)
                .order_by(Task.created_at.desc())
                .all()
            )

            if tasks:
                console.print(f"[bold]Tasks for Project '{project_slug}':[/bold]")
                for task in tasks:
                    console.print(
                        f"- [cyan]{task.title}[/cyan] (Status: {task.status}, Priority: {task.priority})"
                    )
            else:
                console.print(
                    f"[yellow]No tasks found for project '{project_slug}'.[/yellow]"
                )
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            session.close()
