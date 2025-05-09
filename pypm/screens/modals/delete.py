from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class DeleteModalScreen(ModalScreen[bool]):
    BINDINGS = [
        ("e", "edit_project", "Edit project"),
        ("d", "delete_project", "Delete project"),
        ("n", "new_task", "New task"),
        ("escape", "dismiss(False)", "Back to previous screen"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.message = "Are you sure you want to delete this item?"
        self.confirm_label = "Delete"

    def set_message(self, message: str) -> None:
        self.message = message
        self.refresh(recompose=True)

    def set_confirm_label(self, label: str) -> None:
        self.confirm_label = label
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.message, id="message"),
            Button(self.confirm_label, variant="error", id="confirm"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(True)
        elif event.button.id == "cancel":
            self.dismiss(False)
