from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static

from pypm.db import Database
from pypm.screens.home import HomeScreen
from pypm.screens.project_create import ProjectCreateScreen
from pypm.screens.project_detail import ProjectDetailScreen
from pypm.services.project import ProjectService
from pypm.services.task import TaskService


class PyPMApp(App):
    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self):
        super().__init__()

        # Initialize database
        self.db = Database()
        self.db.create_tables()

        # Initialize services
        self.project_service = ProjectService(self.db)
        self.task_service = TaskService(self.db, self.project_service)

        # Fetch projects
        self.projects = self.project_service.list()

    def on_mount(self) -> None:
        self.install_screen(HomeScreen(), name="home")
        self.install_screen(ProjectCreateScreen(), name="project_create")
        self.install_screen(ProjectDetailScreen(), name="project_detail")
        self.push_screen("home")
        self.refresh_bindings()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = PyPMApp()
    app.run()
