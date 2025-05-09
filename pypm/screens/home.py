from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Static,
    Header,
    Footer,
    ListView,
    ListItem,
)


class HomeScreen(Screen):
    BINDINGS = [
        ("n", "new_project", "Create new project"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to PyPM")
        yield Static("Press 'n' to create a new project.")
        with ListView(id="project_list"):
            yield ListItem(Static("Project 1"), id="project_1")
            yield ListItem(Static("Project 2"), id="project_2")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item
        self.app.push_screen("project_detail")

    def action_new_project(self) -> None:
        self.app.push_screen("project_create")
