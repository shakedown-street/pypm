from textual.app import App

from pypm.db import init_db
from pypm.screens.home import HomeScreen
from pypm.screens.modals.delete import DeleteModalScreen
from pypm.screens.project_create import ProjectCreateScreen
from pypm.screens.project_detail import ProjectDetailScreen
from pypm.services.project import ProjectService
from pypm.services.task import TaskService


class PyPMApp(App):
    """
    Main entry point for the Textual/TUI application.
    """

    CSS_PATH = "tui.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self):
        super().__init__()

        # Initialize database
        init_db()

        # Initialize screens
        self.SCREENS["home"] = HomeScreen()
        self.SCREENS["project_create"] = ProjectCreateScreen()
        self.SCREENS["project_detail"] = ProjectDetailScreen()
        self.SCREENS["delete_modal_screen"] = DeleteModalScreen()

    def on_mount(self) -> None:
        # Install screens
        self.install_screen(self.SCREENS["home"], name="home")
        self.install_screen(self.SCREENS["project_create"], name="project_create")
        self.install_screen(self.SCREENS["project_detail"], name="project_detail")
        self.install_screen(
            self.SCREENS["delete_modal_screen"], name="delete_modal_screen"
        )

        # Push the home screen
        self.push_screen("home")
        self.refresh_bindings()

    def action_toggle_dark(self) -> None:
        """
        Toggle between light and dark themes.
        """
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = PyPMApp()
    app.run()
