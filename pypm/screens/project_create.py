from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Input, Static, RadioSet, RadioButton, Header, Footer


class ProjectCreateScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back to previous screen"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Create a New Project")
        yield Input(id="input_name", placeholder="Project name")
        yield Static("[bold]Slug:[/bold] ", id="project_slug")
        with RadioSet(id="radioset_status"):
            yield RadioButton("Active", value="active")
            yield RadioButton("Inactive", value="inactive")
            yield RadioButton("Archived", value="archived")
        yield Button("Create", id="btn_create")
        yield Footer()
