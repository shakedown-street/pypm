import argparse

from pypm.controllers.project import ProjectController
from pypm.controllers.task import TaskController
from pypm.db import init_db
from pypm.services.project import ProjectService
from pypm.services.task import TaskService


def main():
    """
    Main entry point for the CLI program.
    """

    # Initialize database
    init_db()

    # Initialize services
    project_service = ProjectService()
    task_service = TaskService(project_service)

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

    # Get project command
    get_parser = project_subparsers.add_parser("get", help="Get a project by slug")
    get_parser.add_argument("slug", type=str, help="Slug of the project")
    get_parser.set_defaults(func=projects.get)

    # Update project command
    update_parser = project_subparsers.add_parser(
        "update", help="Update a project by slug"
    )
    update_parser.add_argument("slug", type=str, help="Slug of the project")
    update_parser.add_argument(
        "--name", type=str, help="New name of the project", default=None
    )
    update_parser.add_argument(
        "--status",
        type=str,
        help="New status of the project (active, inactive)",
        choices=["active", "inactive", "completed"],
        default=None,
    )
    update_parser.set_defaults(func=projects.update)

    # Delete project command
    delete_parser = project_subparsers.add_parser(
        "delete", help="Delete a project by slug"
    )
    delete_parser.add_argument("slug", type=str, help="Slug of the project")
    delete_parser.set_defaults(func=projects.delete)

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
    list_task_parser.add_argument(
        "--project",
        type=str,
        help="Project slug",
        default=None,
    )
    list_task_parser.set_defaults(func=tasks.list)

    # Get task command
    get_task_parser = task_subparsers.add_parser("get", help="Get a task by ID")
    get_task_parser.add_argument("id", type=int, help="Task ID")
    get_task_parser.set_defaults(func=tasks.get)

    # Update task command
    update_task_parser = task_subparsers.add_parser(
        "update", help="Update a task by ID"
    )
    update_task_parser.add_argument("id", type=int, help="Task ID")
    update_task_parser.add_argument(
        "--title", type=str, help="New title of the task", default=None
    )
    update_task_parser.add_argument(
        "--body", type=str, help="New body of the task", default=None
    )
    update_task_parser.add_argument(
        "--status",
        type=str,
        help="New status of the task (todo, in_progress, done, blocked)",
        choices=["todo", "in_progress", "done", "blocked"],
        default=None,
    )
    update_task_parser.add_argument(
        "--priority",
        type=str,
        help="New priority of the task (low, medium, high)",
        choices=["low", "medium", "high"],
        default=None,
    )
    update_task_parser.add_argument(
        "--due_date",
        type=str,
        help="New due date of the task (YYYY-MM-DD)",
        default=None,
    )
    update_task_parser.set_defaults(func=tasks.update)

    # Delete task command
    delete_task_parser = task_subparsers.add_parser(
        "delete", help="Delete a task by ID"
    )
    delete_task_parser.add_argument("id", type=int, help="Task ID")
    delete_task_parser.set_defaults(func=tasks.delete)

    # Parse arguments and route to the appropriate function
    args = parser.parse_args()
    if args.resource and args.action:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
