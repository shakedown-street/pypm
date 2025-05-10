from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, ListView, Static

from pypm.services.project import ProjectService


class HomeScreen(Screen):
    BINDINGS = [
        ("n", "new_project", "New project"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to PyPM")
        yield Static("Press 'n' to create a new project.")
        yield DataTable(id="project_table", cursor_type="row")
        yield Footer()

    def on_mount(self) -> None:
        self.projects = ProjectService.list()

        table = self.query_one("#project_table", DataTable)
        table.add_column("Name")
        table.add_column("Slug")
        table.add_column("Status")
        table.add_column("ID")

        for project in self.projects:
            table.add_row(project.name, project.slug, project.status, project.id)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        selected = event.cursor_row
        slug = self.projects[selected].slug
        self.app.push_screen("project_detail")
        self.app.SCREENS["project_detail"].set_project(slug)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item
        slug = selected.id.split("project_")[1]
        self.app.push_screen("project_detail")
        self.app.SCREENS["project_detail"].set_project(slug)

    def action_new_project(self) -> None:
        self.app.push_screen("project_create")
