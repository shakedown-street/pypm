from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, ListItem, ListView, Static

from pypm.services.project import ProjectService


class HomeScreen(Screen):
    BINDINGS = [
        ("n", "new_project", "New project"),
    ]

    def __init__(self, project_service: ProjectService):
        super().__init__()
        self.project_service = project_service
        self.projects = self.project_service.list()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to PyPM")
        yield Static("Press 'n' to create a new project.")
        with ListView(id="project_list"):
            for project in self.projects:
                yield ListItem(Static(project.name), id=f"project_{project.slug}")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item
        slug = selected.id.split("project_")[1]
        self.app.SCREENS["project_detail"].set_project(slug)
        self.app.push_screen("project_detail")

    def action_new_project(self) -> None:
        self.app.push_screen("project_create")
