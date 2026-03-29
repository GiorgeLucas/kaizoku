import subprocess
from typing import Any, Union

from rich.text import Text
from textual import events, work
from textual.app import ComposeResult
from textual.screen import ModalScreen, Screen
from textual.widgets import DataTable, Input, LoadingIndicator, OptionList

from kaizoku.core.anime import Anime, Episode
from kaizoku.scraping import SearchManager
from kaizoku.ui.widgets import EpisodesInfoContainer, EpisodesTableContainer


class EpisodeQualityModal(ModalScreen[str]):
    BINDINGS = [("escape", "dismiss(None)", "Close")]
    options: list

    DEFAULT_CSS = """
        #option_list {
            background: transparent;
            border: round ansi_green;
            width: 50%;
            margin: 0 0;

            & > .option-list--option {
                background: transparent;
                color: ansi_magenta;
            }

            & > .option-list--option-highlighted {
                background: ansi_magenta;
                color: ansi_black;
            }

            &:focus > .option-list--option-highlighted {
                color: ansi_black;
            }

            & > .option-list--option-hover {
                background: ansi_white;
                color: ansi_black;
            }
        }
    """

    def __init__(self, options):
        super().__init__()
        self.options = options

    def compose(self) -> ComposeResult:
        optionsList = OptionList(*self.options, id="option_list")
        optionsList.border_title = "Select Quality"
        yield optionsList

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(str(event.option.prompt))


class EpisodesScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen()", "Back")]
    anime: Anime

    filtered_episodes_dict: dict[str, Episode]
    episodes_dict: dict[str, Episode]

    def __init__(self, anime: Anime):
        super().__init__()
        self.anime = anime
        self.filtered_episodes_dict = {}
        self.episodes_dict = {}

    def compose(self) -> ComposeResult:
        yield LoadingIndicator()
        yield EpisodesInfoContainer(id="info-container")
        yield EpisodesTableContainer(id="table-container")

    def on_mount(self):
        self.query_one("#info-container", EpisodesInfoContainer).display = False
        self.query_one("#table-container", EpisodesTableContainer).display = False
        self.get_episodes(self.anime)

    def on_key(self, event: events.Key):
        table = self.query_one("#episodes_list", DataTable)

        if event.key in ("up", "down"):
            event.prevent_default()
            table.focus()
        elif event.key in ("enter"):
            event.prevent_default()
            table.focus()
            selected_episode = self.query_one(
                "#info-container", EpisodesInfoContainer
            ).episode
            self.get_episode_playdata(selected_episode)
        else:
            if event.is_printable:
                event.prevent_default()
                (input := self.query_one("#episode_search", Input)).focus()
                input.value += event.character if event.character is not None else ""
                input.cursor_position = len(input.value)

    def on_input_changed(self, event: Input.Changed):
        query = event.value.lower().strip()
        table = self.query_one("#episodes_list", DataTable)

        table.clear()

        if len(query) > 0:
            self.filtered_episodes_dict = {
                url: episode
                for url, episode in self.episodes_dict.items()
                if query in episode.title.lower()
            }

            for url, episode in self.filtered_episodes_dict.items():
                table.add_row(
                    Text(episode.title, overflow="ellipsis", no_wrap=True), key=url
                )
        else:
            for url, episode in self.episodes_dict.items():
                table.add_row(
                    Text(episode.title, overflow="ellipsis", no_wrap=True), key=url
                )

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        if event.row_key.value is not None:
            key = event.row_key.value
            episode = self.episodes_dict[key]
            self.get_episode_playdata(episode)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted):
        if event.row_key.value is not None:
            key = event.row_key.value
            episode = self.episodes_dict[key]
            self.query_one("#info-container", EpisodesInfoContainer).episode = episode

    def update_episodes_datatable(self, episodes_list: list[Episode]):
        episodes_datatable = self.query_one("#episodes_list", DataTable)
        for episode in episodes_list:
            key = episode.page_link
            self.episodes_dict[key] = episode
            episodes_datatable.add_row(
                Text(episode.title, overflow="ellipsis", no_wrap=True), key=key
            )
        self.query_one("LoadingIndicator").display = False
        self.query_one("#info-container", EpisodesInfoContainer).display = True
        self.query_one("#table-container", EpisodesTableContainer).display = True
        episodes_datatable.focus()

    def show_quality_modal(self, episode_playdata: Union[dict[str, Any], None]):
        if episode_playdata is not None:
            qualities = episode_playdata.keys()

            def open_mpv(quality: str | None) -> None:
                if quality is not None:
                    self.exec_mpv(episode_playdata[quality])

            self.app.push_screen(EpisodeQualityModal(qualities), open_mpv)

    @work(thread=True)
    async def exec_mpv(self, url: str):
        try:
            subprocess.Popen(
                ["mpv", url],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.app.call_from_thread(
                self.app.notify, "MPV started.", severity="information"
            )
        except FileNotFoundError:
            self.app.call_from_thread(
                self.app.notify, "MPV not found. Please install it.", severity="error"
            )
        except Exception as e:
            self.app.call_from_thread(
                self.app.notify, f"Error starting MPV: {e}", severity="error"
            )

    @work(exclusive=True, thread=True)
    async def get_episodes(self, anime: Anime):
        episodes_list = SearchManager.search_episodes(anime)
        if len(episodes_list) > 0:
            self.app.call_from_thread(self.update_episodes_datatable, episodes_list)
        else:
            self.app.call_from_thread(
                lambda: (
                    self.app.pop_screen(),
                    self.app.notify(
                        f"No episodes of the anime [bold ansi_magenta]{anime.title}[/bold ansi_magenta] were found.",
                        timeout=3,
                    ),
                )
            )

    @work(exclusive=True, thread=True)
    async def get_episode_playdata(self, episode: Episode) -> dict[str, Any] | None:
        episode_url = SearchManager.get_play_options(episode)
        self.app.call_from_thread(self.show_quality_modal, episode_url)
