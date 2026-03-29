from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import DataTable


class AnimesTableContainer(Container):
    BORDER_TITLE = "Anime List"

    DEFAULT_CSS = """
        #animes_list > .datatable--hover {
            background: ansi_white;
            color: ansi_black;
        }
    """

    PROVIDER_COLUMN_WIDTH = 16
    LANGUAGE_COLUMN_WIDTH = 13
    TABLE_MARGIN = 10

    def compose(self) -> ComposeResult:
        yield DataTable(id="animes_list", cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one("#animes_list", DataTable)
        columns = [
            (
                "Name",
                self.app.size.width
                - self.PROVIDER_COLUMN_WIDTH
                - self.LANGUAGE_COLUMN_WIDTH
                - self.TABLE_MARGIN,
            ),
            ("Provider", self.PROVIDER_COLUMN_WIDTH),
            ("Language", self.LANGUAGE_COLUMN_WIDTH),
        ]
        for label, width in columns:
            table.add_column(label, width=width)
