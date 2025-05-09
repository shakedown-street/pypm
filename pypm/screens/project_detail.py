from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static,
    Header,
    Footer,
    ListView,
    ListItem,
)


class ProjectDetailScreen(Screen):
    BINDINGS = [
        ("e", "edit_project", "Edit project"),
        ("d", "delete_project", "Delete project"),
        ("escape", "app.pop_screen", "Back to previous screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("[bold]Project Name[/bold]")
        yield Static("[bold]ID:[/bold] 1")
        yield Static("[bold]Tasks:[/bold]")
        with ListView(id="task_list"):
            yield ListItem(Static("Task 1"), id="task_1")
            yield ListItem(Static("Task 2"), id="task_2")
        yield Footer()

    def action_edit_project(self) -> None:
        self.app.log("Edit project action triggered")

    def action_delete_project(self) -> None:
        self.app.log("Delete project action triggered")
