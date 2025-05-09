from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static,
    Header,
    Footer,
    ListView,
    ListItem,
)

from pypm.services.project import ProjectService


class ProjectDetailScreen(Screen):
    BINDINGS = [
        ("e", "edit_project", "Edit"),
        ("d", "delete_project", "Delete"),
        ("n", "new_task", "New task"),
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
        yield Static("[bold]Tasks:[/bold]")
        with ListView(id="task_list"):
            yield ListItem(Static("Task 1"), id="task_1")
            yield ListItem(Static("Task 2"), id="task_2")
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
