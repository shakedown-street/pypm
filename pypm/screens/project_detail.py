from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from pypm.services.project import ProjectService
from pypm.services.task import TaskService


class ProjectDetailScreen(Screen):
    BINDINGS = [
        ("e", "edit_project", "Edit"),
        ("d", "delete_project", "Delete"),
        ("n", "new_task", "New task"),
        ("l", "load_tasks", "Load tasks"),
        ("escape", "app.pop_screen", "Back to previous screen"),
    ]

    def __init__(self):
        super().__init__()
        self.project = None

    def set_project(self, slug: str) -> None:
        self.project = ProjectService.get_by_slug(slug)
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(f"[bold]{self.project.name}[/bold]")
        yield Static(f"[bold]ID:[/bold] {self.project.id}")
        yield DataTable(id="task_table", cursor_type="row")
        yield Footer()

    def action_edit_project(self) -> None:
        self.app.log("Edit project action triggered")

    def action_delete_project(self) -> None:
        def confirm_delete(confirm: bool | None) -> None:
            if confirm:
                ProjectService.delete(self.project.id)

        self.app.SCREENS["delete_modal_screen"].set_message(
            f"Are you sure you want to delete {self.project.name}?"
        )
        self.app.push_screen(self.app.SCREENS["delete_modal_screen"], confirm_delete)

    def action_load_tasks(self) -> None:
        try:
            table = self.query_one("#task_table", DataTable)
            table.clear(columns=True)

            table.add_column("Title")
            table.add_column("Created At")
            table.add_column("Due Date")
            table.add_column("Priority")
            table.add_column("Status")
            table.add_column("ID")

            tasks = TaskService.list(self.project.slug)
            for task in tasks:
                table.add_row(
                    task.title,
                    task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A",
                    task.priority,
                    task.status,
                    str(task.id),
                )
        except Exception as e:
            self.app.log(f"Error loading tasks: {e}")
