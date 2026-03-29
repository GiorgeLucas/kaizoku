# Kaizoku

A TUI (Terminal User Interface) application for searching and watching anime from multiple streaming providers.

## ✨ Features

- Search anime titles across multiple providers
- Browse episodes for selected anime
- Choose from available video qualities
- Launch videos in external player (mpv)
- Extensible provider architecture
- Color-coded UI showing provider and language information
- Real-time episode filtering

## 📦 Installation

### From PyPI (once published)

```bash
pip install kaizoku
```

### From source

```bash
git clone <repository-url>
cd kaizoku
pip install -e .
```

### Requirements

- Python 3.11 or higher
- mpv (optional, for video playback)

## 🚀 Usage

After installation, run:

```bash
kaizoku
```

This launches the TUI application. The interface consists of:

1. **Search screen**: Enter an anime name to search across all providers
2. **Results table**: Shows matching anime with title, provider, and language
3. **Episodes screen**: Select an anime to see its episodes
4. **Quality selection**: Choose video quality to launch in mpv

### Navigation

- `↑/↓` - Navigate tables
- `Enter` - Select row / open episode options
- `Escape` - Go back / close modal
- Type to filter episodes on the episodes screen

## 📁 Project Structure

```
kaizoku/
├── __main__.py              # Application entry point
├── core/
│   └── anime.py            # Data models (Anime, Episode)
├── providers/
│   ├── common.py           # BaseProvider abstract class, Language enum
│   ├── animefire.py        # Animefire provider implementation
│   └── animesdigital.py   # AnimesDigital provider implementation
├── scraping/
│   └── search_manager.py   # Manages searching across providers
└── ui/
    ├── kaizoku_app.py      # Main Textual App
    ├── screens/
    │   ├── anime_screen.py     # Anime search screen
    │   └── episodes_screen.py  # Episode list and playback
    └── widgets/
        └── ...              # Custom widget containers
```

## ⚙️ Configuration

There is currently no configuration file. The application uses default settings and requires no environment variables.

### Adding Providers

To add a new provider, create a class that inherits from `BaseProvider` in `kaizoku.providers.common` and implement the required methods:

- `search_anime(anime_name: str) -> list[Anime]`
- `search_episodes(anime: Anime) -> list[Episode]`
- `get_play_options(episode: Episode) -> dict[str, str]`

Then add it to the `providers` list in `SearchManager`:

```python
class SearchManager:
    providers: list[BaseProvider] = [Animefire(), AnimesDigital(), YourProvider()]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please ensure your code follows the existing style and includes appropriate testing where applicable.

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
