from textual.app import App, ComposeResult
from textual.widgets import Button, Footer, Header, Input, Label, Static

from pypm.db import Database
from pypm.services.project import ProjectService
from pypm.services.task import TaskService


class PyPM(App):
    def __init__(self):
        super().__init__()

        # Initialize database
        self.db = Database()
        self.db.create_tables()

        # Initialize services
        self.project_service = ProjectService(self.db)

        # Fetch projects
        self.projects = self.project_service.list()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to PyPM!")
        for project in self.projects:
            yield Label(f"Project: {project.name} (Slug: {project.slug})")
        yield Footer()


if __name__ == "__main__":
    app = PyPM()
    app.run()
