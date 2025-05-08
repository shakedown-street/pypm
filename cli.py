import argparse

from pypm.controllers.project import ProjectController
from pypm.controllers.task import TaskController
from pypm.db import Database
from pypm.services.project import ProjectService
from pypm.services.task import TaskService


def main():
    # Initialize database
    db = Database()
    db.create_tables()

    # Initialize services
    project_service = ProjectService(db)
    task_service = TaskService(db, project_service)

    # Initialize controllers
    projects = ProjectController(project_service)
    tasks = TaskController(task_service)

    # Initialize CLI parser
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(title="Resources", dest="resource")

    # Project resource
    project_parser = subparsers.add_parser("project", help="Manage projects")
    project_subparsers = project_parser.add_subparsers(title="Actions", dest="action")

    # Create project command
    create_parser = project_subparsers.add_parser("create", help="Create a new project")
    create_parser.add_argument("name", type=str, help="Name of the project")
    create_parser.set_defaults(func=projects.create)

    # List projects command
    list_parser = project_subparsers.add_parser("list", help="List all projects")
    list_parser.set_defaults(func=projects.list)

    # Task resource
    task_parser = subparsers.add_parser("task", help="Manage tasks")
    task_subparsers = task_parser.add_subparsers(title="Actions", dest="action")

    # Create task command
    create_task_parser = task_subparsers.add_parser("create", help="Create a new task")
    create_task_parser.add_argument("project_slug", type=str, help="Project slug")
    create_task_parser.add_argument("title", type=str, help="Title of the task")
    create_task_parser.add_argument(
        "--body", type=str, help="Body of the task", default=""
    )
    create_task_parser.add_argument(
        "--status",
        type=str,
        help="Status of the task (todo, in_progress, done, blocked)",
        choices=["todo", "in_progress", "done", "blocked"],
        default="todo",
    )
    create_task_parser.add_argument(
        "--priority",
        type=str,
        help="Priority of the task (low, medium, high)",
        choices=["low", "medium", "high"],
        default="medium",
    )
    create_task_parser.add_argument(
        "--due_date",
        type=str,
        help="Due date of the task (YYYY-MM-DD)",
        default=None,
    )
    create_task_parser.set_defaults(func=tasks.create)

    # List tasks command
    list_task_parser = task_subparsers.add_parser(
        "list", help="List all tasks for a project"
    )
    list_task_parser.add_argument("project_slug", type=str, help="Project slug")
    list_task_parser.set_defaults(func=tasks.list)

    # Parse arguments and route to the appropriate function
    args = parser.parse_args()
    if args.resource and args.action:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
